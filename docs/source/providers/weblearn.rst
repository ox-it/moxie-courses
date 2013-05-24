WebLearn
========

WebLearn (Sakai) is a provider available for booking some presentations.

Making a request to the API
---------------------------

All requests should be made requesting JSON (by specifying the HTTP header “Accept: application/json”).

Handling errors from the API
----------------------------

When requesting JSON and in case of an error, some errors will be returned with a description in JSON
(see `original "documentation" <https://github.com/ox-it/wl-course-signup/blob/master/tool/src/main/java/uk/ac/ox/oucs/vle/CustomExceptionMapper.java>`_):

* if the access to the resource is forbidden (HTTP 403)
* if the resource has not been found (HTTP 404)

For these errors, you will get a JSON response containing:

* `status` property: “failed”
* `message` property: a user-friendly message

All other exceptions will return an HTML response, you will have to handle the response code.

Booking a course
----------------

POST request to `/course/cobomo/XXX/booking` where `XXX` is the course ID.

Form parameters:

* `message`: mandatory message where the user should explain the reasons to book a course
* `supervisorEmail` is only mandatory if`supervisorApproval` is `true` when you request details on one course.

Returns an object where the `status` property can be:

* `WAITING`: if the component is full
* `PENDING`: in any other case

Getting information on one course
---------------------------------

Request to `/course/cobomo/XXX` where `XXX` is the course ID.

Contains a property `supervisorApproval` which will determine if asking the user for the email address of its supervisor is mandatory.

The response contains a property `supervisorApproval` which determines if asking the user for

Getting information on booked course for one user
-------------------------------------------------

Status can be `WITHDRAWN` (meaning that the user has withdrawn his booking, and can book *again* the presentation).

Withdrawing a booked course
---------------------------

When a student withdraw a course, he cannot book the same course again, he would have to ask the course administrator to re-instate them.
