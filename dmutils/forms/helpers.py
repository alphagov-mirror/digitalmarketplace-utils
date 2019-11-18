
from collections import OrderedDict


def remove_csrf_token(data):
    """Flask-WTF==0.14.2 now includes `csrf_token` in `form.data`, whereas previously wtforms explicitly didn't do
    this. When we pass form data straight through to the API, the API often carries out strict validation and doesn't
    like to see `csrf_token` in the input. So this helper will strip it out of a dict, if it's present.

    Example:
    >>> remove_csrf_token(form.data)
    """
    cleaned_data = {**data}

    if 'csrf_token' in data:
        del cleaned_data['csrf_token']

    return cleaned_data


def get_errors_from_wtform(form):
    """Converts errors from a Flask-WTForm into the same format we generate from content-loader forms.

    Returns a dictionary that includes three keys: `input_name`, `question`,
    and `message`. The dictionary should be passed to the template as `errors`.

    This allows us to treat errors from both content-loader forms and wtforms
    the same way inside templates.

    We also include in the dictionary errors in a format suitable for GOV.UK
    Frontend components:

        # app.py
        class Form(FlaskForm):
            input = DMTextInput()

        @flask.route("/")
        def view():
            form = Form()
            errors = get_errors_from_wtform()
            return render(
                "template.html",
                errors=errors,
            )

        # template.html
        {{ govukErrorSummary({
            "errorList": errors.values()
        }) }}

        {{ govukTextInput({
            "errorMessage": errors.input.errorMessage,
        }) }}

    :param form: A Flask-WTForm
    :return: A dict with error information in a form suitable for Digital Marketplace templates
    """
    return OrderedDict(
        # TODO: remove legacy code (items for frontend toolkit validation banners, 'input-' prefix)
        (
            key,
            {
                # parameters for digitalmarketplace-frontend-toolkit template toolkit/forms/validation.html
                "input_name": key, "question": form[key].label.text, "message": form[key].errors[0],

                # parameters for govuk-frontend macro govukErrorSummary
                "text": form[key].errors[0], "href": f"#input-{key}",

                # parameters for govuk-frontend errorMessage parameter
                "errorMessage": (
                    {"text": form[key].errors[0]}
                    if form[key].errors[0]
                    else {}
                )
            }
        )
        for key in
        form.errors.keys()
    )
