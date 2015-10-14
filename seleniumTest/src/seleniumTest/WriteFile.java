package seleniumTest;

import java.util.Arrays;
import java.util.List;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;
import java.util.Map;
import java.util.TreeMap;
import java.util.HashMap;
import java.util.Set;
import java.util.Iterator;
import java.util.Scanner;

public class WriteFile {
  public static void main(String[] args) {
    try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("output", true)))) {
        out.println("the text");
    }catch (IOException e) {
        System.err.println(e);
    }
    System.out.println("Hi");
  }
}

