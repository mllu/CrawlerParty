package seleniumTest;

import java.io.*;
import java.util.*;
import java.lang.System;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.firefox.internal.ProfilesIni;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class ASPXHandler {

	public static void main(String[] args) {
		// Create a new instance of Firefox Browser
		// WebDriver driver = new FirefoxDriver();
		ProfilesIni profileObj = new ProfilesIni();
		FirefoxProfile yourFFProfile = profileObj.getProfile("your profile");
		WebDriver driver = new FirefoxDriver(yourFFProfile);
		processDriver(driver);
		driver.quit();
	}

	public static void processDriver(WebDriver driver) {
		System.out.println("=========== Into ASPXHandler ==========");

		// Get the current page URL and store the value in variable 'url'
		// String url = driver.getCurrentUrl();
		String url = "http://www.jasonsguns.com/Search.aspx?code=Firearms";
		// http://www.jasonsguns.com/Search.aspx?code=Knives
		// http://www.jasonsguns.com/Search.aspx?code=Optics
		// http://www.jasonsguns.com/Search.aspx?code=Ammo
		// http://www.jasonsguns.com/Search.aspx?code=Reload
		// http://www.jasonsguns.com/Search.aspx?code=Wanted
		// http://www.jasonsguns.com/Search.aspx?code=Trade
		// http://www.jasonsguns.com/Search.aspx?code=Access
		// http://www.jasonsguns.com/Search.aspx?code=Hunting
		// Print the value of variable in the console
		System.out.println("[ASPXHandler][processDriver] The current URL is: " + url);

		// Load a new page in the current browser windows
		driver.get(url);
		
		try {
			System.out.println("[ASPXHandler][processDriver] before sleep");
			Thread.sleep(1000);
			System.out.println("[ASPXHandler][processDriver] after sleep");

		} catch (Exception e) {
			System.out.println("[ASPXHandler][processDriver] Exception caught");
		}

		if (url.indexOf("Search.aspx") != -1) {
			// find all listing post link
			List<WebElement> findListings = driver.findElements(By.className("listingRow"));
			System.out.println("[ASPXHandler][processDriver] total listings Found: " + findListings.size());
			// log listings to /tmp/outlinks
			try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("/tmp/outlinks", true)))) {
				// this are all the links you like to visit
				int count = 0;
				for (WebElement elem : findListings) {
					count++;
					String onClick = elem.getAttribute("onclick");
					String replaced = onClick.replace("\"", "").replace("window.location =.", "");
					String newURL = "http://www.jasonsguns.com" + replaced;
					System.out.println(newURL);
					out.println(newURL);
					driver.get(newURL);
					(new WebDriverWait(driver, 10)).until(ExpectedConditions.presenceOfElementLocated(By.id("page")));
					break;
					// String[] parts = replaced.split("=");
					// for (String part : parts)
					// System.out.println(part);
				}
				System.out.println("[ASPXHandler][processDriver] " + findListings.size() + " listings shown");
				System.out.println("[ASPXHandler][processDriver] total listings Logged: " + count);
			} catch (IOException e) {
				System.err.println(e);
			}
		}

		url = driver.getCurrentUrl();
		if (url.indexOf("Display.aspx") != -1) {
			// find all image element
			List<WebElement> findImages = driver.findElements(By.xpath("//img"));
			System.out.println("[ASPXHandler][processDriver] total images Found: " + findImages.size());

			try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("/tmp/images", true)))) {
				// show all the links of image
				int count = 0;
				for (WebElement elem : findImages) {
					String src = elem.getAttribute("src");
					if (src.indexOf("ImageDisplay") != -1) {
						count++;
						System.out.println(src);
						out.println(src);
					}
				}
				System.out.println("[ASPXHandler][processDriver] " + count + " images logged");
			} catch (IOException e) {
				System.err.println(e);
			}
		}
		/*
		 * try { System.out.println("[ASPXHandler][processDriver] before sleep"
		 * ); Thread.sleep(1000); System.out.println(
		 * "[ASPXHandler][processDriver] after sleep");
		 * 
		 * } catch (Exception e) { System.out.println(
		 * "[ASPXHandler][processDriver] Exception caught"); }
		 */
	}
}
