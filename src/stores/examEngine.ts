import { ref, reactive } from 'vue';
import { db, type ExamHistory, type Question } from '../db';
import allQuestions from '../assets/data/all_questions.json';
import { recordQuestionResult } from './errorBook';

// Simple store using Vue Reactivity
export const examState = reactive({
  isActive: false,
  startTime: 0,
  endTime: 0,
  questions: [] as Question[],
  currentIndex: 0,
  answers: {} as Record<string, any>,
  score: 0,
  isFinished: false
});

// timeRemaining 必须是模块级单例：timerInterval 也是模块级的，
// 若把 ref 放在 useExamEngine() 内部，组件重建后会拿到新的空 ref，
// 而定时器仍写入旧实例 → 界面倒计时永远停在 00:00。
export const timeRemaining = ref(0);

let timerInterval: number | undefined;

export const useExamEngine = () => {

  const generateExamPaper = () => {
    const allQs = allQuestions as Question[];
    const tfQuestions = allQs.filter(q => q.type === 'true_false');
    // 外国驾照切换（外免切替）知识确认：50 道判断题（Fisher-Yates 洗牌）。
    const shuffled = [...tfQuestions];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    // 同一图片在 50 题内只出现一次，避免「同一标志图既判对又判错」的重复感
    const usedImg = new Set<string>();
    const paper: Question[] = [];
    for (const q of shuffled) {
      if (paper.length >= 50) break;
      const img = q.image_url;
      if (img) {
        if (usedImg.has(img)) continue;
        usedImg.add(img);
      }
      paper.push(q);
    }
    return paper;
  };

  const initExam = async () => {
    examState.questions = generateExamPaper();
    examState.currentIndex = 0;
    examState.answers = {};
    examState.score = 0;
    examState.isFinished = false;
    examState.isActive = true;
    
    // 外免切替知识确认考试时间为 30 分钟
    examState.startTime = Date.now();
    examState.endTime = examState.startTime + 30 * 60 * 1000;
    
    startTimer();
  };

  const startTimer = () => {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = window.setInterval(updateTimer, 1000);
    updateTimer(); // Initial call
  };

  const updateTimer = () => {
    if (!examState.isActive) return;
    
    const now = Date.now();
    const diff = examState.endTime - now;
    
    if (diff <= 0) {
      timeRemaining.value = 0;
      finishExam();
    } else {
      timeRemaining.value = diff;
    }
  };

  const finishExam = async () => {
    if (examState.isFinished) return;

    examState.isActive = false;
    examState.isFinished = true;
    if (timerInterval) clearInterval(timerInterval);
    
    calculateScore();

    const history: ExamHistory = {
      date: Date.now(),
      score: examState.score,
      totalTimeMs: Math.max(0, Date.now() - examState.startTime),
      details: examState.questions.map(question => ({
        questionId: question.id,
        correct: isAnswerCorrect(question, examState.answers[question.id])
      }))
    };

    try {
      await db.transaction('rw', db.examHistory, db.errorBook, async () => {
        await db.examHistory.add(history);
        for (const detail of history.details) {
          await recordQuestionResult(detail.questionId, detail.correct);
        }
      });
    } catch (error) {
      console.error('Failed to save exam result', error);
    }
  };

  const isAnswerCorrect = (question: Question, answer: any) => {
    if (question.type === 'true_false' || !question.sub_questions?.length) {
      return typeof question.answer === 'boolean' && answer === question.answer;
    }

    return Array.isArray(answer)
      && question.sub_questions.every((subQuestion, index) => subQuestion.answer === answer[index]);
  };

  const calculateScore = () => {
    let currentScore = 0;
    
    examState.questions.forEach(q => {
      const ans = examState.answers[q.id];
      if (isAnswerCorrect(q, ans)) {
        currentScore += q.type === 'hazard_prediction' ? 2 : 1;
      }
    });
    
    examState.score = currentScore;
  };

  const nextQuestion = () => {
    if (examState.currentIndex < examState.questions.length - 1) {
      examState.currentIndex++;
    } else {
      finishExam();
    }
  };

  const prevQuestion = () => {
    if (examState.currentIndex > 0) {
      examState.currentIndex--;
    }
  };

  const setAnswer = (questionId: string, answer: any) => {
    examState.answers[questionId] = answer;
  };

  const formatTime = (ms: number) => {
    const totalSeconds = Math.floor(ms / 1000);
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const s = (totalSeconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  return {
    examState,
    timeRemaining,
    initExam,
    finishExam,
    nextQuestion,
    prevQuestion,
    setAnswer,
    formatTime
  };
};
