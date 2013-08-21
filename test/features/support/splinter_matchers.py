from hamcrest.core.base_matcher import BaseMatcher


class ElementHasText(BaseMatcher):

    def __init__(self, expected_text):
        self.expected_text = expected_text

    def _matches(self, element):
        return self.expected_text in element.text

    def describe_to(self, description):
        description.append_text('text ').append_description_of(self.expected_text)

    def describe_mismatch(self, element, mismatch_description):
        mismatch_description.append_text('was ').append_description_of(element.text)


class ElementHasClass(BaseMatcher):

    def __init__(self, expected_class):
        self.expected_class = expected_class

    def _matches(self, element):
        return element.has_class(self.expected_class)

    def describe_to(self, description):
        description.append_text('class ').append_description_of(self.expected_class)

    def describe_mismatch(self, element, mismatch_description):
        mismatch_description.append_text('was ').append_description_of(element.first['class'])


def has_text(text):
    return ElementHasText(text)


def has_class(clazz):
    return ElementHasClass(clazz)