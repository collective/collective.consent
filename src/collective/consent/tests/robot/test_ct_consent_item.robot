# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.consent -t test_consent_item.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.consent.testing.COLLECTIVE_CONSENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/consent/tests/robot/test_consent_item.robot
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

Scenario: As a site administrator I can add a Consent Item
  Given a logged-in site administrator
    and an add Consents Container form
   When I type 'My Consent Item' into the title field
    and I submit the form
   Then a Consent Item with the title 'My Consent Item' has been created

Scenario: As a site administrator I can view a Consent Item
  Given a logged-in site administrator
    and a Consent Item 'My Consent Item'
   When I go to the Consent Item view
   Then I can see the Consent Item title 'My Consent Item'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Consents Container form
  Go To  ${PLONE_URL}/++add++Consents Container

a Consent Item 'My Consent Item'
  Create content  type=Consents Container  id=my-consent_item  title=My Consent Item

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Consent Item view
  Go To  ${PLONE_URL}/my-consent_item
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Consent Item with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Consent Item title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
