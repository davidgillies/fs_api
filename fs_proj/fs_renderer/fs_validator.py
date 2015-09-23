import time


class Validator(object):
    def __init__(self, questions, data):
        self.data = data
        self.questions = questions
        self.errors = {}

    def is_valid(self):
        valid = True
        for k in self.data:
            if k != 'id':
                for test in self.questions[k].tests:
                    result, error = self.do_test(test)(self.questions[k], self.data[k])
                    if result is False:
                        self.errors[k] = error
                        valid = False
        return valid

    def do_test(self, test):
        return {'CheckMaxLength': self.maxlength, 'IsAnswered': self.required,
                'type': self.test_type}[test]

    def maxlength(self, question, answer):
        if len(answer) > int(question.maxlength):
            return (False, 'Your answer should be less than %s characters long' % question.maxlength)
        else:
            return (True, None)

    def required(self, question, answer):
        if question.required and not answer:
            return (False, 'Please give an answer')
        else:
            return (True, None)

    def test_type(self, question, answer):
        return self.get_type_test(question.data_type['type'])(answer)
        
    def get_type_test(self, the_type):
        return {'integer': self.check_int, 'string': self.check_str, 'date': self.check_date, 'datetime': self.check_time}[the_type]
        
    def check_date(self, date_value):
        masks = ['%Y%m%d','%Y-%m-%d','%d%m%Y','%m%d%Y']
        # change to use question.pattern and use this format in XML
        return self.check_format(date_value, masks)

    def check_time(self, time_value):
        masks = ['%H:%M']
        return self.check_format(time_value, masks)
        
    def check_format(self, value, masks):
        format_ok = False
        error = 'Incorrect Format'
        for mask in masks:
            try:
                time.strptime(value, mask)
                format_ok = True
                error = None
                break
            except:
                pass
        return (format_ok, error)

    def check_str(self, string_value):
        return (True, None)

    def check_int(self, string_value):
        return (True, None)
