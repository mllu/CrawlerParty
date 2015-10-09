package seleniumTest;

import java.util.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;

public class IdClick {
	public static void main(String[] args) {

		// Create a new instance of Firefox Browser
		WebDriver driver = new FirefoxDriver();

		// Open the URL in firefox browser
		driver.get("http://mllu.elasticbeanstalk.com/crawlerTest/");
		//driver.get("file:///home/mllu/Downloads/seleniumTest/crawlerTest.html");
		
		// Maximize the Browser window
//		driver.manage().window().maximize();

		// Get the current page URL and store the value in variable 'str'
		String str = driver.getCurrentUrl();

		// Print the value of variable in the console
		System.out.println("The current URL is " + str);

		By.ById id = new By.ById("pic");
		// tag.tagName("button");
		List<WebElement> list = driver.findElements(id);
		for (WebElement elem : list) {
			System.out.print("click elem with tag: " + elem.getTagName());
			System.out.println(" @ " + elem.toString());
			if (elem.getSize().getWidth() != 0 && elem.getSize().getWidth() != 0 && elem.isDisplayed()) {
				
//				JavascriptExecutor jse = (JavascriptExecutor)driver;
//				jse.executeScript("document.getElementById('pic1').click();");
				elem.click();
			}
		}
	}
}
