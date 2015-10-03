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
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;

public class DefaultHandler implements InteractiveSeleniumHandler {
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
}
