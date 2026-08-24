import { db, type ErrorRecord } from '../db';
import { LEGACY_QUESTION_IDS } from '../utils/questionIds';

/**
 * 艾宾浩斯记忆曲线复习调度：
 * 答错 → 进入/回到第 0 阶段（立即再练）
 * 连续答对 → 按固定间隔推进：5分钟 → 30分钟 → 12小时 → 1天 → 2天 → 4天 → 7天 → 15天
 * 走完全部阶段 → 毕业，移出错题本
 */
const MIN = 60 * 1000;
const HOUR = 60 * MIN;
export const DAY_MS = 24 * HOUR;

export const EBBINGHAUS_STAGES: { label: string; ms: number }[] = [
  { label: '5分钟后', ms: 5 * MIN },
  { label: '30分钟后', ms: 30 * MIN },
  { label: '12小时后', ms: 12 * HOUR },
  { label: '1天后', ms: 1 * DAY_MS },
  { label: '2天后', ms: 2 * DAY_MS },
  { label: '4天后', ms: 4 * DAY_MS },
  { label: '7天后', ms: 7 * DAY_MS },
  { label: '15天后', ms: 15 * DAY_MS }
];

/** 兼容旧记录：补齐 stage 字段 */
export const migrateLegacyErrorBookRecords = async () => {
  await db.transaction('rw', db.errorBook, async () => {
    for (const [legacyId, currentId] of Object.entries(LEGACY_QUESTION_IDS)) {
      const legacy = await db.errorBook.get(legacyId);
      if (!legacy) continue;
      const current = await db.errorBook.get(currentId);
      if (!current || legacy.lastReviewDate > current.lastReviewDate) {
        await db.errorBook.put({ ...legacy, id: currentId, questionId: currentId });
      }
      await db.errorBook.delete(legacyId);
    }
    // 旧记录可能没有 stage 字段：用 consecutiveCorrect 近似还原
    const all = await db.errorBook.toArray();
    for (const rec of all) {
      if (typeof rec.stage !== 'number') {
        await db.errorBook.put({ ...rec, stage: Math.min(rec.consecutiveCorrect || 0, EBBINGHAUS_STAGES.length - 1) });
      }
    }
  });
};

export const recordQuestionResult = async (questionId: string, correct: boolean) => {
  const now = Date.now();
  const existing = await db.errorBook.get(questionId);

  if (!correct) {
    const record: ErrorRecord = {
      id: questionId,
      questionId,
      consecutiveCorrect: 0,
      stage: 0,
      lastReviewDate: now,
      nextReviewDate: now + EBBINGHAUS_STAGES[0].ms, // 5分钟后重新出现
      easeFactor: existing?.easeFactor ?? 2.5,
      interval: 0
    };
    await db.errorBook.put(record);
    return { removed: false, record };
  }

  if (!existing) return { removed: false, record: null }; // 首次就答对不进错题本

  const stage = (existing.stage ?? existing.consecutiveCorrect ?? 0) + 1;

  if (stage >= EBBINGHAUS_STAGES.length) {
    // 走完艾宾浩斯曲线全部阶段 → 毕业
    await db.errorBook.delete(questionId);
    return { removed: true, record: null };
  }

  const record: ErrorRecord = {
    ...existing,
    consecutiveCorrect: existing.consecutiveCorrect + 1,
    stage,
    lastReviewDate: now,
    nextReviewDate: now + EBBINGHAUS_STAGES[stage].ms,
    interval: Math.round(EBBINGHAUS_STAGES[stage].ms / DAY_MS)
  };
  await db.errorBook.put(record);
  return { removed: false, record };
};

/** 当前到期待复习的题数 */
export const countDueReviews = async (): Promise<number> => {
  const now = Date.now();
  return db.errorBook.where('nextReviewDate').belowOrEqual(now).count();
};
