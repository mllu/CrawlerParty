/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.nutch.protocol.interactiveselenium;

import java.util.*;
<<<<<<< HEAD:nutch/src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers/DefaultHandler.java
import java.util.StringTokenizer;

//import org.openqa.selenium.WebDriver;
=======
>>>>>>> 156e01b9bf05de7c79e4e5041b27214dec4f7d80:src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers/DefaultHandler.java
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class DefaultHandler implements InteractiveSeleniumHandler {
<<<<<<< HEAD:nutch/src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers/DefaultHandler.java
    /*
    public void processDriver(WebDriver driver) {}
    public boolean shouldProcessURL(String URL) {
        return true;
    }
    */
    public void processDriver(WebDriver driver) {
        System.out.println("@@@@@@@@@@ The current URL is @@@@@@@@@@@: ");
       /*
         * Should be divide into two parts:
         * interact with JavaScripts (click on element)
         * submit forms (sendKeys and subimt)
       */

        //Get the current page URL and store the value in variable 'url'
        String url = driver.getCurrentUrl();

        //Print the value of variable in the console
        System.out.println("@@@@@@@@@@ The current URL is @@@@@@@@@@@: " + url);

        //Load a new page in the current browser windows
        driver.get(url);

        // click image
        /*
        //Maximize the Browser window
        //driver.manage().window().maximize();
        By.ById id = new By.ById("pic");
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
        */

        WebElement element = driver.findElement(By.name("searchtext"));
        element.sendKeys("rifle\n"); // send also a "\n"

        WebElement myDynamicElement = (new WebDriverWait(driver, 10))
                .until(ExpectedConditions.presenceOfElementLocated(By.id("searchlist")));// searchlist

        try {
            System.out.println("before sleep");
            Thread.sleep(3000);
            System.out.println("after sleep");

        } catch (Exception e) {
            System.out.println("Exception caught");
        }

        // List<WebElement> findElements = driver.findElements(By.xpath("//img"));
        List<WebElement> findElements = driver
                .findElements(By.xpath(".//*[@id='searchlist']/center/table/tbody/tr/td/img"));
        System.out.println("total Results Found: " + findElements.size());

        // this are all the links you like to visit
        for (WebElement elem : findElements) {

            if (elem.getSize().getWidth() != 0 && elem.getSize().getWidth() != 0 && elem.isDisplayed()) {
                // String parent = driver.getWindowHandle();
                // elem.click();
                // waitForWindow(driver);
                // switchToModalDialog(driver, parent);
                // driver.manage().timeouts().implicitlyWait(30,
                // TimeUnit.SECONDS);
                // System.out.println(elem.toString());
            }

            System.out.println(elem.getAttribute("src"));
            // System.out.println(elem.toString());
        }

    }

    public boolean shouldProcessURL(String URL) {
        System.out.println("!!!!!!!!!!URL!!!!!!!!!!!!!");
        System.out.println(URL);
//        return !URL.isEmpty();
        return true;
    }
=======
	public void processDriver(WebDriver driver) {
		System.out.println("=========== Into Default Handler ==========");
		driver.get(driver.getCurrentUrl()); //load a new page in the current browser windows
		searchBarFinder(driver);
	}

	public boolean shouldProcessURL(String URL) {
		System.out.println("Defualt Handler : " + URL);
		return !URL.isEmpty();
	}

	private static void searchBarFinder(WebDriver driver){
		WebElement form = driver.findElement(By.tagName("form"));
		WebElement input = form.findElement(By.tagName("input"));
		input.clear();
		input.sendKeys("gun");
		form.submit();
	}
>>>>>>> 156e01b9bf05de7c79e4e5041b27214dec4f7d80:src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers/DefaultHandler.java
}
