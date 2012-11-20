from datetime import datetime

from moxie_courses.course import Course, Presentation

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
        if 'presentation_bookingEndpoint' in result:
            presentation.booking_endpoint = result['presentation_bookingEndpoint']
        course.presentations.append(presentation)
    return course