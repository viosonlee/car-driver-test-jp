import { ref, reactive } from 'vue';
import { db, type ExamHistory, type Question } from '../db';
import allQuestions from '../assets/data/all_questions.json';

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

let timerInterval: number | undefined;

export const useExamEngine = () => {
  const timeRemaining = ref(0);

  const generateExamPaper = () => {
    const allQs = allQuestions as Question[];
    const tfQuestions = allQs.filter(q => q.type === 'true_false');
    // 外国驾照切换（外免切替）知识确认：50 道判断题。
    return [...tfQuestions].sort(() => 0.5 - Math.random()).slice(0, 50);
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
      await db.examHistory.add(history);
    } catch (error) {
      console.error('Failed to save exam history', error);
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
