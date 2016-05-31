from . import models
import generator.models
import school.models
import questionnaire.models
from modules.entrance.models import EntranceStatus
from generator import generator
import datetime


class DocumentGenerator:
    def __init__(self, school):
        self.school = school
        self.payment_questionnaire = questionnaire.models.Questionnaire.objects.filter(
            for_school=self.school,
            short_name='payment'
        ).first()

        self.enrolled_questionnaire = questionnaire.models.Questionnaire.objects.filter(
            for_school=self.school,
            short_name='enrolled'
        ).first()

        self.payment_questions = questionnaire.models.AbstractQuestionnaireQuestion.objects.filter(
            questionnaire=self.payment_questionnaire
        )
        self.payment_questions = {q.short_name: q for q in self.payment_questions}

        self.questionnaire_choice_variants = list(
            questionnaire.models.ChoiceQuestionnaireQuestionVariant.objects.filter(
                question__questionnaire=self.payment_questionnaire
            )
        )
        self.questionnaire_choice_variants = {v.id: v for v in self.questionnaire_choice_variants}

    # Return just user's answer if it's a text, integer or date,
    # otherwise return corresponding option from ChoiceQuestionnaireQuestionVariant
    def _get_payment_question_answer(self, user_answer):
        question_short_name = user_answer.question_short_name
        question = self.payment_questions[question_short_name]

        if isinstance(question, questionnaire.models.ChoiceQuestionnaireQuestion):
            return self.questionnaire_choice_variants[int(user_answer.answer)].text

        return user_answer.answer

    def generate(self, document_type, user):
        if not self.payment_questionnaire.is_filled_by(user):
            raise ValueError('User has not fill the payment questionnaire')

        user_payment_questionnaire = list(
            questionnaire.models.QuestionnaireAnswer.objects.filter(
                questionnaire=self.payment_questionnaire,
                user=user
            )
        )
        user_payment_questionnaire = {
            a.question_short_name: self._get_payment_question_answer(a)
            for a in user_payment_questionnaire
        }

        user_enrolled_questionnaire = list(
            questionnaire.models.QuestionnaireAnswer.objects.filter(
                questionnaire=self.enrolled_questionnaire,
                user=user
            )
        )
        user_enrolled_questionnaire = {
            a.question_short_name: a.answer
            for a in user_enrolled_questionnaire
        }
        # Only for 2016:
        user.last_name = user_enrolled_questionnaire['last_name']
        user.first_name = user_enrolled_questionnaire['first_name']
        user.middle_name = user_enrolled_questionnaire['middle_name']

        entrance_status = EntranceStatus.objects.filter(
            for_school=self.school,
            for_user=user,
        ).first()
        if entrance_status is None or entrance_status.status != EntranceStatus.Status.ENROLLED:
            raise ValueError('User has not enrolled')

        session = entrance_status.session

        price = models.PaymentAmount.get_amount_for_user(self.school, user)

        g = generator.TemplateGenerator(document_type.template)
        return g.generate({
            'school': self.school,
            'session': session,
            'student': user,
            'contract': {
                'id': user.id,
                'created_at': datetime.date.today()
            },
            'payment': user_payment_questionnaire,
            'price': price
        })



