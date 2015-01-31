# What is this?

This is a small Flask app to gather username of people wanting a badge at an event.


# Setting up

1. Create an OpenShift app (or any other mod_wsgi host)
2. Set environment variables BADGE, AUTH_KEY and ADMIN_KEY (openshift: "rhc set-env -a localbadge BADGE=badge AUTH_KEY=somekey ADMIN_KEY=key")
3. Enjoy
