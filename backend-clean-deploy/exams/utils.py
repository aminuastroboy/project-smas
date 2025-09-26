THRESHOLD = 50.0

def grade_question(question, answer):
    if question.is_mcq:
        try:
            if answer is None:
                return 0
            return question.marks if str(answer).strip().lower() == str(question.correct_answer).strip().lower() else 0
        except:
            return 0
    try:
        return float(answer) if answer is not None else 0
    except:
        return 0

def compute_breakdown(exam, answers):
    topic_totals = {}
    topic_scores = {}
    question_scores = []
    for q in exam.questions.all():
        topic = q.topic.name if q.topic else 'General'
        topic_totals.setdefault(topic, 0)
        topic_scores.setdefault(topic, 0)
        topic_totals[topic] += q.marks
    for q in exam.questions.all():
        qid = str(q.id)
        ans = answers.get(qid) or answers.get(int(qid)) or None
        score = grade_question(q, ans)
        topic = q.topic.name if q.topic else 'General'
        topic_scores[topic] += score
        question_scores.append({'question_id': q.id, 'score': score, 'max': q.marks})
    topic_percent = {t: (topic_scores[t] / topic_totals[t] * 100) if topic_totals[t] > 0 else 0 for t in topic_totals}
    weak_topics = [t for t,p in topic_percent.items() if p < THRESHOLD]
    return {
        'question_scores': question_scores,
        'topic_scores': {t: {'score': topic_scores[t], 'max': topic_totals[t], 'percent': round(topic_percent[t],1)} for t in topic_totals},
        'weak_topics': weak_topics,
    }
