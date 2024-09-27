import contextlib
import logging
import random
import time

from selenium.common import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.browser import Browser
from src.utils import CONFIG, Utils

ACTIVITY_TITLE_TO_SEARCH = {
    "Search the lyrics of a song": "black sabbath supernaut lyrics",
    "Translate anything": "translate pencil sharpener to spanish",
    "Let's watch that movie again!": "aliens movie",
    "Discover open job roles": "walmart open job roles",
    "Plan a quick getaway": "flights nyc to paris",
    "You can track your package": "usps tracking",
    "Find somewhere new to explore": "directions to new york",
    "Too tired to cook tonight?": "Pizza Hut near me",
    "Quickly convert your money": "convert 374 usd to yen",
    "Learn to cook a new recipe": "how cook pierogi",
    "Find places to stay": "hotels rome italy",
    "How's the economy?": "sp 500",
    "Who won?": "braves score",
    "Gaming time": "vampire survivors video game",
    "What time is it?": "china time",
    "Houses near you": "apartments manhattan",
    "Get your shopping done faster": "new iphone",
    "Expand your vocabulary": "define polymorphism",
    "Stay on top of the elections": "election news latest",
    "Prepare for the weather": "weather tomorrow",
}


class Activities:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver

    def click_element_if_visible(self, element):
        try:
            if element.is_displayed() and element.is_enabled():
                element.click()
                logging.info("Dashboard pop-up registered and closed, needs to be done once on new accounts")
            else:
                pass
        except (ElementNotInteractableException, NoSuchElementException):
            pass

    def dashboardPopUpModalCloseCross(self):
        try:

            element = self.webdriver.find_element(By.CSS_SELECTOR, ".dashboardPopUpPopUpSelectButton")
            self.click_element_if_visible(element)
            time.sleep(0.25)
        except NoSuchElementException:
            return





    def openDailySetActivity(self, cardId: int):
        # Open the Daily Set activity for the given cardId
        cardId += 1
        element = self.webdriver.find_element(By.XPATH,
                                              f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardId}]/div/card-content/mee-rewards-daily-set-item-content/div/a', )
        # element = self.webdriver.find_element(By.CSS_SELECTOR,
        #                                       f".ng-scope:nth-child(8) .ng-scope:nth-child({cardId}) .contentContainer:nth-child(3) > .ng-binding:nth-child({cardId})")
        # element = self.webdriver.find_element(By.XPATH,
        #                                       f"//div[@id=\'daily-sets\']/mee-card-group/div/mee-card[{cardId}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div[{cardId}]/p")
        self.browser.utils.click(element)
        self.browser.utils.switchToNewTab(timeToWait=8)

    def openMorePromotionsActivity(self, cardId: int):
        # Open the More Promotions activity for the given cardId
        element = self.webdriver.find_element(By.CSS_SELECTOR,
                                              f"#more-activities > .m-card-group > .ng-scope:nth-child({cardId + 1}) .ds-card-sec")
        self.browser.utils.click(element)
        self.browser.utils.switchToNewTab(timeToWait=8)

    def completeSearch(self):
        # Simulate completing a search activity
        time.sleep(random.randint(10, 15))
        self.browser.utils.closeCurrentTab()

    def completeSurvey(self):
        # Simulate completing a survey activity
        # noinspection SpellCheckingInspection
        self.webdriver.find_element(By.ID, f"btoption{random.randint(0, 1)}").click()
        time.sleep(random.randint(10, 15))
        self.browser.utils.closeCurrentTab()

    def completeQuiz(self):
        # Simulate completing a quiz activity
        with contextlib.suppress(TimeoutException):
            startQuiz = self.browser.utils.waitUntilQuizLoads()
            self.browser.utils.click(startQuiz)
        # this is bugged on Chrome for some reason
        self.browser.utils.waitUntilVisible(
            By.ID, "overlayPanel", 5
        )
        currentQuestionNumber: int = self.webdriver.execute_script(
            "return _w.rewardsQuizRenderInfo.currentQuestionNumber"
        )
        maxQuestions = self.webdriver.execute_script(
            "return _w.rewardsQuizRenderInfo.maxQuestions"
        )
        numberOfOptions = self.webdriver.execute_script(
            "return _w.rewardsQuizRenderInfo.numberOfOptions"
        )
        for _ in range(currentQuestionNumber, maxQuestions + 1):
            if numberOfOptions == 8:
                answers = []
                for i in range(numberOfOptions):
                    isCorrectOption = self.webdriver.find_element(
                        By.ID, f"rqAnswerOption{i}"
                    ).get_attribute("iscorrectoption")
                    if isCorrectOption and isCorrectOption.lower() == "true":
                        answers.append(f"rqAnswerOption{i}")
                for answer in answers:
                    element = self.webdriver.find_element(By.ID, answer)
                    self.browser.utils.click(element)
                    self.browser.utils.waitUntilQuestionRefresh()
            elif numberOfOptions in [2, 3, 4]:
                correctOption = self.webdriver.execute_script(
                    "return _w.rewardsQuizRenderInfo.correctAnswer"
                )
                for i in range(numberOfOptions):
                    if (
                        self.webdriver.find_element(
                            By.ID, f"rqAnswerOption{i}"
                        ).get_attribute("data-option")
                        == correctOption
                    ):
                        element = self.webdriver.find_element(By.ID, f"rqAnswerOption{i}")
                        self.browser.utils.click(element)

                        self.browser.utils.waitUntilQuestionRefresh()
                        break
        self.browser.utils.closeCurrentTab()

    def completeABC(self):
        # Simulate completing an ABC activity
        counter = self.webdriver.find_element(
            By.XPATH, '//*[@id="QuestionPane0"]/div[2]'
        ).text[:-1][1:]
        numberOfQuestions = max(int(s) for s in counter.split() if s.isdigit())
        for question in range(numberOfQuestions):
            element = self.webdriver.find_element(By.ID, f"questionOptionChoice{question}{random.randint(0, 2)}")
            self.browser.utils.click(element)
            time.sleep(random.randint(10, 15))
            element = self.webdriver.find_element(By.ID, f"nextQuestionbtn{question}")
            self.browser.utils.click(element)
            time.sleep(random.randint(10, 15))
        time.sleep(random.randint(1, 7))
        self.browser.utils.closeCurrentTab()

    def completeThisOrThat(self):
        # Simulate completing a This or That activity
        startQuiz = self.browser.utils.waitUntilQuizLoads()
        self.browser.utils.click(startQuiz)
        self.browser.utils.waitUntilVisible(
            By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10
        )
        time.sleep(random.randint(10, 15))
        for _ in range(10):
            correctAnswerCode = self.webdriver.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer"
            )
            answer1, answer1Code = self.getAnswerAndCode("rqAnswerOption0")
            answer2, answer2Code = self.getAnswerAndCode("rqAnswerOption1")
            answerToClick: WebElement
            if answer1Code == correctAnswerCode:
                answerToClick = answer1
            elif answer2Code == correctAnswerCode:
                answerToClick = answer2

            self.browser.utils.click(answerToClick)
            time.sleep(random.randint(10, 15))

        time.sleep(random.randint(10, 15))
        self.browser.utils.closeCurrentTab()

    def getAnswerAndCode(self, answerId: str) -> tuple[WebElement, str]:
        # Helper function to get answer element and its code
        answerEncodeKey = self.webdriver.execute_script("return _G.IG")
        answer = self.webdriver.find_element(By.ID, answerId)
        answerTitle = answer.get_attribute("data-option")
        return (
            answer,
            self.browser.utils.getAnswerCode(answerEncodeKey, answerTitle),
        )

    def doActivity(self, activity: dict, activities: list[dict]) -> None:
        try:
            activityTitle = (
                activity["title"].replace("\u200b", "").replace("\xa0", " ")
            )
            logging.debug(f"activityTitle={activityTitle}")
            if activity["complete"] is True or activity["pointProgressMax"] == 0:
                logging.debug("Already done, returning")
                return
            # Open the activity for the activity
            cardId = activities.index(activity)
            isDailySet = "daily_set_date" in activity["attributes"]
            if isDailySet:
                self.openDailySetActivity(cardId)
            else:
                self.openMorePromotionsActivity(cardId)
            self.browser.webdriver.execute_script("window.scrollTo(0, 1080)")
            with contextlib.suppress(TimeoutException):
                searchbar = self.browser.utils.waitUntilClickable(
                    By.ID, "sb_form_q"
                )
                self.browser.utils.click(searchbar)
            # todo These and following are US-English specific, maybe there's a good way to internationalize
            if activityTitle in ACTIVITY_TITLE_TO_SEARCH:
                searchbar.send_keys(ACTIVITY_TITLE_TO_SEARCH[activityTitle])
                searchbar.submit()
            elif "poll" in activityTitle:
                logging.info(f"[ACTIVITY] Completing poll of card {cardId}")
                # Complete survey for a specific scenario
                self.completeSurvey()
            elif activity["promotionType"] == "urlreward":
                # Complete search for URL reward
                self.completeSearch()
            elif activity["promotionType"] == "quiz":
                # Complete different types of quizzes based on point progress max
                if activity["pointProgressMax"] == 10:
                    self.completeABC()
                elif activity["pointProgressMax"] in [30, 40]:
                    self.completeQuiz()
                elif activity["pointProgressMax"] == 50:
                    self.completeThisOrThat()
            else:
                # Default to completing search
                self.completeSearch()
            self.browser.webdriver.execute_script("window.scrollTo(0, 1080)")
            time.sleep(random.randint(5, 10))
        except Exception:
            logging.error(
                f"[ACTIVITY] Error doing {activityTitle}", exc_info=True
            )
        self.browser.utils.resetTabs()
        time.sleep(2)

    def completeActivities(self):
        logging.info("[DAILY SET] " + "Trying to complete the Daily Set...")
        dailySetPromotions = self.browser.utils.getDailySetPromotions()
        self.browser.utils.goToRewards()
        self.dashboardPopUpModalCloseCross()
        for activity in dailySetPromotions:
            self.doActivity(activity, dailySetPromotions)
        logging.info("[DAILY SET] Done")

        logging.info("[MORE PROMOS] " + "Trying to complete More Promotions...")
        morePromotions: list[dict] = self.browser.utils.getMorePromotions()
        self.browser.utils.goToRewards()
        for activity in morePromotions:
            self.doActivity(activity, morePromotions)
        logging.info("[MORE PROMOS] Done")

        if CONFIG.get("apprise").get("notify").get("incomplete-promotions"):
            incompleteActivities: list[tuple[str, str]] = []
            for activity in (self.browser.utils.getDailySetPromotions() +
                             self.browser.utils.getMorePromotions()):  # Have to refresh
                if activity["pointProgress"] < activity["pointProgressMax"]:
                    incompleteActivities.append(
                        (activity["title"], activity["promotionType"])
                    )
            if incompleteActivities:
                Utils.sendNotification(
                    f"We found some incomplete activities for {self.browser.username} to do!",
                    incompleteActivities,
                )

