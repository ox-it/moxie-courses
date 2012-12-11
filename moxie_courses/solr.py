from datetime import datetime

from moxie_courses.domain import Course, Presentation

SOLR_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def presentations_to_course_object(solr_response):
    """Transform a list of presentations from Solr to a Course object
    :param solr_response: dict from Solr
    :return Course object
    """
    reference = solr_response[0]
    course = Course(reference['course_identifier'])
    course.title = reference['course_title']
    course.description = reference['course_description']
    course.provider = reference['provider_title']
    course.subjects = reference['course_subject']
    for result in solr_response:
        presentation = Presentation(result['presentation_identifier'], course)
        if 'presentation_start' in result:
            presentation.start = datetime.strptime(result['presentation_start'], SOLR_DATE_FORMAT)
        if 'presentation_end' in result:
            presentation.end = datetime.strptime(result['presentation_end'], SOLR_DATE_FORMAT)
        if 'presentation_applyFrom' in result:
            presentation.apply_from = datetime.strptime(result['presentation_applyFrom'], SOLR_DATE_FORMAT)
        if 'presentation_applyUntil' in result:
            presentation.apply_until = datetime.strptime(result['presentation_applyUntil'], SOLR_DATE_FORMAT)
        if 'presentation_bookingEndpoint' in result:
            presentation.booking_endpoint = result['presentation_bookingEndpoint']
        course.presentations.append(presentation)
    return course


def presentation_to_presentation_object(solr_response):
    """Transform one document from Solr as a Presentation/Course object
    :param solr_response: document from Solr
    :return Presentation/Course object
    """
    course = Course(solr_response['course_identifier'])
    course.title = solr_response['course_title']
    course.description = solr_response['course_description']
    course.provider = solr_response['provider_title']
    course.subjects = solr_response['course_subject']
    presentation = Presentation(solr_response['presentation_identifier'], course)
    if 'presentation_start' in solr_response:
        presentation.start = datetime.strptime(solr_response['presentation_start'], SOLR_DATE_FORMAT)
    if 'presentation_end' in solr_response:
        presentation.end = datetime.strptime(solr_response['presentation_end'], SOLR_DATE_FORMAT)
    if 'presentation_applyFrom' in solr_response:
        presentation.apply_from = datetime.strptime(solr_response['presentation_applyFrom'], SOLR_DATE_FORMAT)
    if 'presentation_applyUntil' in solr_response:
        presentation.apply_until = datetime.strptime(solr_response['presentation_applyUntil'], SOLR_DATE_FORMAT)
    if 'presentation_bookingEndpoint' in solr_response:
        presentation.booking_endpoint = solr_response['presentation_bookingEndpoint']
    course.presentations.append(presentation)
    return course