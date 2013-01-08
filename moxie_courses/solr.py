from datetime import datetime
from itertools import izip

from moxie_courses.domain import Course, Presentation, Subject

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
        if 'presentation_memberApplyTo' in result:
            presentation.apply_link = result['presentation_memberApplyTo']
        if 'presentation_attendanceMode' in result:
            presentation.attendance_mode = result['presentation_attendanceMode']
        if 'presentation_attendancePattern' in result:
            presentation.attendance_pattern = result['presentation_attendancePattern']
        if 'presentation_studyMode' in result:
            presentation.study_mode = result['presentation_studyMode']

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
    if 'presentation_memberApplyTo' in solr_response:
        presentation.apply_link = solr_response['presentation_memberApplyTo']
    if 'presentation_attendanceMode' in solr_response:
        presentation.attendance_mode = solr_response['presentation_attendanceMode']
    if 'presentation_attendancePattern' in solr_response:
        presentation.attendance_pattern = solr_response['presentation_attendancePattern']
    if 'presentation_studyMode' in solr_response:
        presentation.study_mode = solr_response['presentation_studyMode']

    course.presentations.append(presentation)
    return course


def subjects_facet_to_subjects_domain(solr_response):
    """Transforms the facetted response from Solr into a list of Subject objects
    :param: solr_response: facetted response from solr.
    :return list of Subjects
    """
    facets = solr_response.as_dict['facet_counts']['facet_fields']['course_subject']
    # Solr returns a list as ['skill A', 2, 'skill B', 5, 'skill C', 3]
    i = iter(facets)
    subjects = [Subject(title, count) for (title, count) in izip(i, i)]
    return subjects
