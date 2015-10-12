/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * <p/>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p/>
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
import java.util.concurrent.TimeUnit;


import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import org.apache.nutch.parse.Outlink;
import org.apache.nutch.parse.OutlinkExtractor;

public class ASPXHandler implements InteractiveSeleniumHandler {

    public void processDriver(WebDriver driver) {
        System.out.println("=========== Into ASPXHandler ==========");
        //Get the current page URL and store the value in variable 'url'
        String url = driver.getCurrentUrl();

        //Print the value of variable in the console
        System.out.println("[ASPXHandler][processDriver] The current URL is: " + url);

        // Load a new page in the current browser windows
        (new WebDriverWait(driver, 10)).until(ExpectedConditions.presenceOfElementLocated(By.id("page")));

        // listing page
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
                    //System.out.println(newURL);
                    out.println(newURL);
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
        // content page
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
                        //System.out.println(src);
                        out.println(src);
                    }
                }
                System.out.println("[ASPXHandler][processDriver] " + count + " images logged");
            } catch (IOException e) {
                System.err.println(e);
            }
        }
    }

    public boolean shouldProcessURL(String URL) {
        return !URL.isEmpty();
    }
}
