# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.consent -t test_consents_container.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.consent.testing.COLLECTIVE_CONSENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/consent/tests/robot/test_consents_container.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Consents Container
  Given a logged-in site administrator
    and an add Consents Container form
   When I type 'My Consents Container' into the title field
    and I submit the form
   Then a Consents Container with the title 'My Consents Container' has been created

Scenario: As a site administrator I can view a Consents Container
  Given a logged-in site administrator
    and a Consents Container 'My Consents Container'
   When I go to the Consents Container view
   Then I can see the Consents Container title 'My Consents Container'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Consents Container form
  Go To  ${PLONE_URL}/++add++Consents Container

a Consents Container 'My Consents Container'
  Create content  type=Consents Container  id=my-consents_container  title=My Consents Container

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Consents Container view
  Go To  ${PLONE_URL}/my-consents_container
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Consents Container with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Consents Container title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
