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

import java.io.*;
import java.util.*;
import java.lang.System;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;


import org.openqa.selenium.*;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import org.apache.nutch.parse.Outlink;
import org.apache.nutch.parse.OutlinkExtractor;

public class BlockPageHandler implements InteractiveSeleniumHandler {
	private static HashMap<String, String> cookieMap = new HashMap<String, String>();
	private static ArrayList<Cookie> cookies = new ArrayList<Cookie>();
	private static String accumulatedData;

	public void processDriver(WebDriver driver, ArrayList<Cookie> cookies) {
		this.cookies = cookies;
		processDriver(driver);
	}
	public void processDriver(WebDriver driver) {
		System.out.println("=========== Into BlockPageHandler's processDriver ==========");
		//Get the current page URL and store the value in variable 'url'
		String url = driver.getCurrentUrl();

		//Print the value of variable in the console
		System.out.println("[BlockPageHandler][processDriver] The current URL is: " + url);
		System.out.println("[BlockPageHandler][processDriver] cookieMap.size() is: " + cookies.size());

		/*
		//for (Map.Entry<String, String> entry : cookieMap.entrySet()) {
		for (Cookie cookie : cookies) {
			System.out.println("Retrieve cookie back!!!");
			printCookie(cookie);
			Cookie ck = new Cookie(
					cookie.getName(),
					cookie.getPath(),
					cookie.getDomain(),
					cookie.getValue(),
					cookie.getExpiry());

			driver.manage().addCookie(ck);
		}
		*/
		driver.get(url);

		/*
		// wait for finsih loading webpage, hard code the timer
		try {
			System.out.println("[SearchBarHandler][processDriver] before sleep");
			Thread.sleep(2000);
			System.out.println("[SearchBarHandler][processDriver] after sleep");

		} catch (Exception e) {
			System.out.println("[SearchBarHandler][processDriver] Exception caught");
		}
		*/

		//if (url.indexOf("tradesnsales") != -1 || url.indexOf("privacy") != -1) {
		if (url.indexOf("privacy") != -1) {
			WebElement myDynamicElement = (new WebDriverWait(driver, 10))
					.until(ExpectedConditions.presenceOfElementLocated(By.id("radio1")));

//		WebElement element = driver.findElement(By.id("radio1"));
			List<WebElement> radios = driver.findElements(By.id("radio1"));
			System.out.println("radios size: " + radios.size());

			for (WebElement radio : radios) {
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
			try {
				System.out.println("[SearchBarHandler][processDriver] before sleep");
				Thread.sleep(3000);
				System.out.println("[SearchBarHandler][processDriver] after sleep");

			} catch (Exception e) {
				System.out.println("[SearchBarHandler][processDriver] Exception caught");
			}

			// log outlinks to /tmp/outlinks
			List<WebElement> findOutlinks = driver.findElements(By.xpath("//a"));
			try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("/tmp/outlinks", true)))) {
				// this are all the links you like to visit
				int count = 0;
				for (WebElement elem : findOutlinks) {
					out.println(elem.getAttribute("href"));
					count++;
				}
				System.out.println("[ListImageHandler][processDriver] total Outlinks Logged: " + count);
			}catch (IOException e) {
				System.err.println(e);
			}

			// append the string to the last page's driver
			JavascriptExecutor jsx = (JavascriptExecutor) driver;
			jsx.executeScript("document.body.innerHTML=document.body.innerHTML "
					+ accumulatedData + ";");

			accumulatedData += driver.findElement(By.tagName("body"))
					.getAttribute("innerHTML");

			/*
			Set<Cookie> cookies = driver.manage().getCookies();
			System.out.println("Size: " + cookies.size());

			Iterator<Cookie> itr = cookies.iterator();
			while (itr.hasNext()) {
				Cookie cookie = itr.next();
				cookies.add(cookie);
				//cookieMap.put(cookie.getName(), cookie.getValue());
				printCookie(cookie);
			}
			*/

		}

		System.out.println("=========== Leave BlockPageHandler's processDriver ==========");

	}

	private void printCookie(Cookie cookie) {
		System.out.println(cookie.getName() + "\n" + cookie.getPath()
				+ "\n" + cookie.getDomain() + "\n" + cookie.getValue()
				+ "\n" + cookie.getExpiry());
	}
	public boolean shouldProcessURL(String URL) {
		System.out.println("BlockPageHandler : " + URL);
		return !URL.isEmpty();
	}

}
