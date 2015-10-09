package seleniumTest;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.firefox.internal.ProfilesIni;

public class JSEngineClick {
	private static ArrayList<Cookie> cookies = new ArrayList<Cookie>();

	public static void main(String[] args) {

		// Create a new instance of Firefox Browser
		// WebDriver driver = new FirefoxDriver();
		ProfilesIni profileObj = new ProfilesIni();
		FirefoxProfile yourFFProfile = profileObj.getProfile("your profile");
		WebDriver driver = new FirefoxDriver(yourFFProfile);
		for (int i = 0; i < 2; i++) {
			processDriver(driver);
		}
		driver.quit();
	}

	public static void processDriver(WebDriver driver) {
		System.out.println("=========== Into BlockPageHandler's processDriver ==========");
		// Get the current page URL and store the value in variable 'url'
		// String url = driver.getCurrentUrl();
		String url = "https://www.tradesnsales.com/category/recreational%2Fguns";

		// Print the value of variable in the console
		System.out.println("[BlockPageHandler][processDriver] cookieMap.size() is: " + cookies.size());

		// for (Map.Entry<String, String> entry : cookieMap.entrySet()) {
		for (Cookie cookie : cookies) {
			System.out.println("Retrieve cookie back!!!");
			printCookie(cookie);
			Cookie ck = new Cookie(cookie.getName(), cookie.getPath(), cookie.getDomain(), cookie.getValue(),
					cookie.getExpiry());

			driver.manage().addCookie(ck);
		}
		driver.get(url);

		// wait for finsih loading webpage, hard code the timer
		try {
			System.out.println("[SearchBarHandler][processDriver] before sleep");
			Thread.sleep(2000);
			System.out.println("[SearchBarHandler][processDriver] after sleep");

		} catch (Exception e) {
			System.out.println("[SearchBarHandler][processDriver] Exception caught");
		}

		// Get the current page URL and store the value in variable 'str'
		String str = driver.getCurrentUrl();

		// Print the value of variable in the console
		System.out.println("[BlockPageHandler][processDriver] The current URL is: " + str);

		// if (url.indexOf("tradesnsales") != -1 || url.indexOf("privacy") !=
		// -1) {
		if (str.indexOf("privacy") != -1) {
			WebElement myDynamicElement = (new WebDriverWait(driver, 10))
					.until(ExpectedConditions.presenceOfElementLocated(By.id("radio1")));

			// WebElement element = driver.findElement(By.id("radio1"));
			List<WebElement> radios = driver.findElements(By.id("radio1"));
			System.out.println("radios size: " + radios.size());

			for (WebElement radio : radios)

			{
				if (radio != null) {// && radio.isDisplayed()) {
					System.out.println("radio Info: " + radio);
					// radio.click(); //hidden radio can not click
					((JavascriptExecutor) driver).executeScript("document.getElementById('radio1').click();");
					driver.findElement(By.className("btn-success")).click();
				} else {
					System.out.println("cant not find element");

				}
			}

			// wait for finsih loading webpage, hard code the timer
			try

			{
				System.out.println("[SearchBarHandler][processDriver] before sleep");
				Thread.sleep(3000);
				System.out.println("[SearchBarHandler][processDriver] after sleep");

			} catch (

			Exception e)

			{
				System.out.println("[SearchBarHandler][processDriver] Exception caught");
			}

			// log outlinks to /tmp/outlinks
			List<WebElement> findOutlinks = driver.findElements(By.xpath("//a"));
			try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("/tmp/outlinks", true))))

			{
				// this are all the links you like to visit
				int count = 0;
				for (WebElement elem : findOutlinks) {
					out.println(elem.getAttribute("href"));
					count++;
				}
				System.out.println("[ListImageHandler][processDriver] total Outlinks Logged: " + count);
			} catch (

			IOException e)

			{
				System.err.println(e);
			}

			Set<Cookie> cookies = driver.manage().getCookies();
			System.out.println("Size: " + cookies.size());

			Iterator<Cookie> itr = cookies.iterator();
			while (itr.hasNext())

			{
				Cookie cookie = itr.next();
				cookies.add(cookie);
				// cookieMap.put(cookie.getName(), cookie.getValue());
				printCookie(cookie);
			}
		}
		System.out.println("=========== Leave BlockPageHandler's processDriver ==========");

	}

	public static void printCookie(Cookie cookie) {
		System.out.println(cookie.getName() + "\n" + cookie.getPath() + "\n" + cookie.getDomain() + "\n"
				+ cookie.getValue() + "\n" + cookie.getExpiry());
	}
}
