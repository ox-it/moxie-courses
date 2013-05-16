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

POST request to /course/cobomo/XXX/booking

Returns an object where the `status` property can be:

* `WAITING`: if the component is full
* `PENDING`: in any other case

Getting information on one course
---------------------------------

Request to /course/cobomo/XXX where XXX is the component ID
