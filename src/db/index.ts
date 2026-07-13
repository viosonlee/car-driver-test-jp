import Dexie, { type Table } from 'dexie';

export interface Question {
  id: string;
  type: 'true_false' | 'hazard_prediction';
  question?: string;
  question_jp?: string;
  answer?: boolean;
  explanation?: string;
  image_url?: string;
  scenario?: string;
  sub_questions?: { question: string; answer: boolean; explanation: string }[];
  tags: string[];
}

export interface ErrorRecord {
  id: string;
  questionId: string;
  consecutiveCorrect: number;
  lastReviewDate: number; // Unix timestamp
  nextReviewDate: number; // Unix timestamp
  easeFactor: number; // SM-2 ease factor
  interval: number; // days
}

export interface ExamHistory {
  id?: number;
  date: number;
  score: number;
  totalTimeMs: number;
  details: { questionId: string; correct: boolean }[];
}

export class AppDatabase extends Dexie {
  questions!: Table<Question, string>;
  errorBook!: Table<ErrorRecord, string>;
  examHistory!: Table<ExamHistory, number>;

  constructor() {
    super('DriverTestDB');
    this.version(1).stores({
      questions: 'id, type, *tags',
      // Composite index for fast querying of items due for review
      errorBook: 'id, questionId, nextReviewDate',
      examHistory: '++id, date'
    });
  }
}

export const db = new AppDatabase();
