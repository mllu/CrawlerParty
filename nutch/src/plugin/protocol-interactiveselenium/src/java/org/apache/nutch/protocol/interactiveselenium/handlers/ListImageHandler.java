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

public class ListImageHandler implements InteractiveSeleniumHandler {
    public static HashSet<String> urlSet = new HashSet<String>();

    public void processDriver(WebDriver driver) {
        System.out.println("=========== Into Handler_vci_classifieds ==========");
        //Get the current page URL and store the value in variable 'url'
        String url = driver.getCurrentUrl();

        //Print the value of variable in the console
        System.out.println("[ListImageHandler][processDriver] The current URL is: " + url);

        //Load a new page in the current browser windows
        driver.get(url);

        // form-input structure for search bar
        WebElement form = driver.findElement(By.tagName("form"));
        List<WebElement> inputs = null;
        if (form != null) {
            inputs = form.findElements(By.tagName("input"));
            for (WebElement elem : inputs) {
                if (elem.isDisplayed()) {
                    elem.clear();
                    elem.sendKeys("gun\n");
                    System.out.println("[ListImageHandler][processDriver] Submit keyword \"gun\"");
                    //form.submit();
                    break;
                }
            }
        }

        // direct input html tag for search bar
        ArrayList<String> possibleName = new ArrayList<String>();
        possibleName.add("q");
        possibleName.add("searchtext");
        possibleName.add("txtSearch");

        WebElement element;
        if (inputs == null) {
            for (int i = 0; i < possibleName.size(); i++) {
                element = driver.findElement(By.name(possibleName.get(i)));
                if (element != null) {
                    // send with "\n" == submit
                    element.sendKeys("gun\n");
                    //element.sendKeys("gun");
                    //form.submit();
                    System.out.println("[ListImageHandler][processDriver] Submit keyword \"gun\"");
                    break;
                }
            }

        }

        // wait for finsih loading webpage, hard code timer
        try {
            System.out.println("[ListImageHandler][processDriver] before sleep");
            Thread.sleep(2000);
            System.out.println("[ListImageHandler][processDriver] after sleep");

        } catch (Exception e) {
            System.out.println("[ListImageHandler][processDriver] Exception caught");
        }

        // find all image element
        List<WebElement> findElements = driver.findElements(By.xpath("//img"));
        if (url.equals("http://www.vci-classifieds.com/")) {
            WebElement myDynamicElement = (new WebDriverWait(driver, 10))
                    .until(ExpectedConditions.presenceOfElementLocated(By.id("searchlist")));
            findElements = driver.findElements(By.xpath(".//*[@id='searchlist']/center/table/tbody/tr/td/img"));
        }
        System.out.println("[ListImageHandler][processDriver] total images Found: " + findElements.size());

        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("/tmp/images", true)))) {
            // show all the links of image
            for (WebElement elem : findElements) {
                out.println(elem.getAttribute("src"));
                // System.out.println(elem.toString());
            }
            System.out.println("[ListImageHandler][processDriver] " + findElements.size() + " images shown");
        }catch (IOException e) {
            System.err.println(e);
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

        //driver.close();
        //System.out.println("[ListImageHandler][processDriver] Close Driver");
    }

    public boolean shouldProcessURL(String URL) {
        addAllUrlIntoSet();
        // print stackTrace
        /*
        for (StackTraceElement ste : Thread.currentThread().getStackTrace())
            System.out.println(ste);
        */
        /*
        System.out.println("[ListImageHandler][shouldProcessURL] URL: " + URL);
        String domain_url = "www.vci-classifieds.com";
        System.out.println(URL.indexOf(domain_url) != -1);
        String seed_url = "http://www.vci-classifieds.com/";
        System.out.println("should process this URL? : "+ URL.equals(seed_url));
        return URL.equals(seed_url);
        */
        System.out.println("[ListImageHandler][shouldProcessURL] should process \"" + URL + "\" ?: " + urlSet.contains(URL));
        //return urlSet.contains(URL);
        return !URL.isEmpty();
    }

    public void addAllUrlIntoSet() {
        /*
        urlSet.add("http://www.4chan.org/k/");
        urlSet.add("http://www.academy.com/");
        urlSet.add("http://www.accurateshooter.com/");
        urlSet.add("http://www.advanced-armanent.com/");
        urlSet.add("http://www.americanlisted.com/");
        urlSet.add("http://www.arguntrader.com/");
        urlSet.add("http://www.armslist.com/");
        urlSet.add("http://www.backpage.com/");
        urlSet.add("http://www.budsgunshop.com/");
        urlSet.add("http://www.buyusedguns.net/");
        urlSet.add("http://www.buyusedguns.net/");
        urlSet.add("http://www.cabelas.com/");
        urlSet.add("http://www.cheaperthandirt.com/");
        urlSet.add("http://www.davidsonsinc.com/");
        urlSet.add("http://www.firearmlist.com/");
        urlSet.add("http://www.firearmslist.com/");
        urlSet.add("http://www.freeclassifieds.com/");
        urlSet.add("http://www.freegunclassifieds.com/");
        urlSet.add("http://www.freegunclaXssifieds.com/");
        urlSet.add("http://www.gandermountain.com/");
        urlSet.add("http://www.gunauction.com/");
        urlSet.add("http://www.gunbroker.com/");
        urlSet.add("http://www.gunbroker.com/");
        urlSet.add("http://www.gundeals.org/");
        urlSet.add("http://www.gunlistings.org/");
        urlSet.add("http://www.gunlistings.org/");
        urlSet.add("http://www.gunsamerica.com/");
        urlSet.add("http://www.gunsinternational.com/");
        urlSet.add("http://www.guntrader.com/");
        urlSet.add("http://www.hipointfirearmsforums.com/");
        urlSet.add("http://www.impactguns.com/");
        urlSet.add("http://www.iwanna.com/");
        urlSet.add("http://www.lionseek.com/");
        urlSet.add("http://www.midwestguntrader.com/");
        urlSet.add("http://www.nationalguntrader.com/");
        urlSet.add("http://www.nationalguntrader.com/");
        urlSet.add("http://www.nextechclassifieds.com/categories/sporting-goods/firearms/");
        urlSet.add("http://www.oodle.com/");
        urlSet.add("http://www.recycler.com/");
        urlSet.add("http://www.shooterswap.com/");
        urlSet.add("http://www.shooting.org/");
        urlSet.add("http://www.slickguns.com/");
        urlSet.add("http://www.wantaddigest.com/");
        urlSet.add("http://www.wikiarms.com/guns/");
        urlSet.add("http://www.abqjournal.com/");
        urlSet.add("http://www.alaskaslist.com/");
        urlSet.add("http://www.billingsthriftynickel.com/");
        urlSet.add("http://www.carolinabargaintrader.net/");
        urlSet.add("http://www.carolinabargaintrader.net/");
        urlSet.add("http://www.clasificadosphoenix.univision.com/");
        urlSet.add("http://www.classifiednc.com/");
        urlSet.add("http://www.classifieds.al.com/");
        urlSet.add("http://www.cologunmarket.com/");
        urlSet.add("http://www.comprayventadearms.com/");
        urlSet.add("http://www.dallasguns.com/");
        urlSet.add("http://www.elpasoguntrader.com/");
        urlSet.add("http://www.fhclassifieds.com/");
        urlSet.add("http://www.floridagunclassifieds.com/");
        urlSet.add("http://www.floridaguntrader.com/");
        urlSet.add("http://floridaguntrader.com/");
        urlSet.add("http://www.gowilkes.com/");
        urlSet.add("http://www.gunidaho.com/");
        urlSet.add("http://www.hawaiiguntrader.com/");
        urlSet.add("http://www.idahogunsforsale.com/");
        */
        urlSet.add("http://www.iguntrade.com/");
        urlSet.add("http://www.jasonsguns.com/");
        urlSet.add("http://www.ksl.com/");
        urlSet.add("http://www.kyclassifieds.com/");
        urlSet.add("http://www.midutahradio.com/tradio/");
        urlSet.add("http://www.midwestgtrader.com/");
        urlSet.add("http://www.montanagunclassifieds.com/");
        urlSet.add("http://www.montanagunsforsale.com/");
        urlSet.add("http://www.mountaintrader.com/");
        urlSet.add("http://www.msguntrader.com/");
        urlSet.add("http://www.ncgunads.com/");
        urlSet.add("http://www.newmexicoguntrader.com/");
        urlSet.add("http://www.nextechclassifieds.com/");
        urlSet.add("http://www.sanjoseguntrader.com/");
        urlSet.add("http://www.tell-n-sell.com/");
        urlSet.add("http://tennesseegunexchange.com/");
        urlSet.add("http://www.theoutdoorstrader.com/");
        urlSet.add("http://www.tradesnsales.com/");
        urlSet.add("http://www.upstateguntrader.com/");
        urlSet.add("http://www.vci-classifieds.com/");
        urlSet.add("http://www.zidaho.com/index.php?a=19");
    }
}
