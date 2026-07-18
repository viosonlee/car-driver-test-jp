export const LEGACY_QUESTION_IDS: Record<string, string> = {
  q_sign_img_1784251082935: 'q_sign_img_auto_stop_t',
  q_sign_img_1784251082936: 'q_sign_img_auto_stop_f',
  q_sign_img_1784251082937: 'q_sign_img_auto_no_entry_t',
  q_sign_img_1784251082938: 'q_sign_img_auto_no_entry_f',
  q_sign_img_1784251082939: 'q_sign_img_auto_one_way_t',
  q_sign_img_1784251082940: 'q_sign_img_auto_one_way_f',
  q_sign_img_1784251082941: 'q_sign_img_auto_speed_limit_50_t',
  q_sign_img_1784251082942: 'q_sign_img_auto_speed_limit_50_f',
  q_sign_img_1784251082943: 'q_sign_img_auto_no_parking_t',
  q_sign_img_1784251082944: 'q_sign_img_auto_no_parking_f',
  q_sign_img_1784251082945: 'q_sign_img_auto_no_stopping_t',
  q_sign_img_1784251082946: 'q_sign_img_auto_no_stopping_f',
  q_sign_img_1784251082947: 'q_sign_img_auto_pedestrian_crossing_t',
  q_sign_img_1784251082948: 'q_sign_img_auto_pedestrian_crossing_f',
  q_sign_img_1784251082949: 'q_sign_img_auto_bicycle_crossing_t',
  q_sign_img_1784251082950: 'q_sign_img_auto_bicycle_crossing_f',
};

export const migrateQuestionId = (questionId: string) => LEGACY_QUESTION_IDS[questionId] ?? questionId;

export const migrateAnswerRecord = (answers: Record<string, unknown>) => Object.fromEntries(
  Object.entries(answers).map(([questionId, answer]) => [migrateQuestionId(questionId), answer])
);
