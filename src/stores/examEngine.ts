import { ref, reactive } from 'vue';
import { type Question } from '../db';
import batch1 from '../assets/data/questions_batch_1.json';

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

export const useExamEngine = () => {
  const timeRemaining = ref(0);
  let timerInterval: number;

  const initExam = async () => {
    // In a real app, randomly select 90 T/F and 5 Hazard from db.
    // For now, load the batch directly.
    examState.questions = batch1 as Question[];
    examState.currentIndex = 0;
    examState.answers = {};
    examState.score = 0;
    examState.isFinished = false;
    examState.isActive = true;
    
    // 50 minutes countdown
    examState.startTime = Date.now();
    examState.endTime = examState.startTime + 50 * 60 * 1000;
    
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

  const finishExam = () => {
    examState.isActive = false;
    examState.isFinished = true;
    if (timerInterval) clearInterval(timerInterval);
    
    calculateScore();
  };

  const calculateScore = () => {
    let currentScore = 0;
    
    examState.questions.forEach(q => {
      const ans = examState.answers[q.id];
      if (q.type === 'true_false') {
        if (ans === q.answer) {
          currentScore += 1;
        }
      } else if (q.type === 'hazard_prediction' && q.sub_questions) {
        // Must get all 3 sub-questions right
        if (Array.isArray(ans) && ans.length === 3) {
          const allCorrect = q.sub_questions.every((sq, idx) => sq.answer === ans[idx]);
          if (allCorrect) {
            currentScore += 2;
          }
        }
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
