import { db, type ErrorRecord } from '../db';

const DAY_MS = 24 * 60 * 60 * 1000;
const REQUIRED_CORRECT = 2;

export const recordQuestionResult = async (questionId: string, correct: boolean) => {
  const now = Date.now();
  const existing = await db.errorBook.get(questionId);

  if (!correct) {
    const record: ErrorRecord = {
      id: questionId,
      questionId,
      consecutiveCorrect: 0,
      lastReviewDate: now,
      nextReviewDate: now,
      easeFactor: existing?.easeFactor ?? 2.5,
      interval: 0
    };
    await db.errorBook.put(record);
    return { removed: false, record };
  }

  if (!existing) return { removed: false, record: null };

  const consecutiveCorrect = existing.consecutiveCorrect + 1;
  if (consecutiveCorrect >= REQUIRED_CORRECT) {
    await db.errorBook.delete(questionId);
    return { removed: true, record: null };
  }

  const interval = consecutiveCorrect === 1 ? 1 : Math.max(1, Math.round(existing.interval * existing.easeFactor));
  const record: ErrorRecord = {
    ...existing,
    consecutiveCorrect,
    lastReviewDate: now,
    nextReviewDate: now + interval * DAY_MS,
    interval
  };
  await db.errorBook.put(record);
  return { removed: false, record };
};

