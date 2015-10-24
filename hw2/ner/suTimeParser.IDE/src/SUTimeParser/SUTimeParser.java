// Uncomment the following line if you are modifing with IDE
//package SUTimeParser;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;

import org.joda.time.Period;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.AnnotationPipeline;
import edu.stanford.nlp.pipeline.TokenizerAnnotator;
import edu.stanford.nlp.time.SUTime;
import edu.stanford.nlp.time.SUTime.Temporal;
import edu.stanford.nlp.time.TimeAnnotations;
import edu.stanford.nlp.time.TimeAnnotator;
import edu.stanford.nlp.time.TimeExpression;
import edu.stanford.nlp.util.CoreMap;

public class SUTimeParser {
	static AnnotationPipeline pipeline = null;
	static HashSet<String> timeSet;
	static ArrayList<String> rangePair;

	private static AnnotationPipeline setupPipeline() {
		try {
			String defs_sutime = "./sutime/defs.sutime.txt";
			String holiday_sutime = "./sutime/english.holidays.sutime.txt";
			String _sutime = "./sutime/english.sutime.txt";
			AnnotationPipeline pipeline = new AnnotationPipeline();
			Properties props = new Properties();
			String sutimeRules = defs_sutime + "," + holiday_sutime + "," + _sutime;
			props.setProperty("sutime.rules", sutimeRules);
			props.setProperty("sutime.binders", "0");
			props.setProperty("sutime.markTimeRanges", "true");
			props.setProperty("sutime.includeRange", "true");
			pipeline.addAnnotator(new TokenizerAnnotator(false));
			pipeline.addAnnotator(new TimeAnnotator("sutime", props));
			return pipeline;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}

	}

	public static void annotateText(String text, String referenceDate) {
		try {
			if (referenceDate == null || referenceDate.isEmpty()) {
				SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
				referenceDate = dateFormat.format(new Date());
			} else {
				SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
				try {
					dateFormat.parse(referenceDate);
				} catch (Exception e) {
					referenceDate = dateFormat.format(new Date());
				}
			}
			if (pipeline != null) {
				Annotation annotation = new Annotation(text);
				annotation.set(CoreAnnotations.DocDateAnnotation.class, referenceDate);
				pipeline.annotate(annotation);
				List<CoreMap> timexAnnsAll = annotation.get(TimeAnnotations.TimexAnnotations.class);
				for (CoreMap cm : timexAnnsAll) {
					try {

						String timeInfo = cm.get(TimeExpression.Annotation.class).getTemporal().toString();
						if (!isAbleToParserStartEndTime(timeInfo))
							continue;
						printParsingInfo(cm);

					} catch (ParseException pe) {
						// not a correct format of "yyyy-MM-dd'T'HH:mm:ss"
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			} else {
				System.out.println("Annotation Pipeline object is NULL");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static void printParsingInfo(CoreMap cm) {
		List<CoreLabel> tokens = cm.get(CoreAnnotations.TokensAnnotation.class);
		String startOffset = tokens.get(0).get(CoreAnnotations.CharacterOffsetBeginAnnotation.class)
				.toString();

		String endOffset = tokens.get(tokens.size() - 1)
				.get(CoreAnnotations.CharacterOffsetEndAnnotation.class).toString();

		Temporal temporal = cm.get(TimeExpression.Annotation.class).getTemporal();

		// System.out.println("Token text : " + cm.toString());
		// System.out.println("Temporal Value : " + temporal.toString());
		// System.out.println("Timex : " + temporal.getTimexValue());
		System.out.println("Timex type : " + temporal.getTimexType().name());
		// System.out.println("Start offset : " + startOffset);
		// System.out.println("End Offset : " + endOffset);
		System.out.println("--");
	}

	private static boolean isAbleToParserStartEndTime(String timeInfo) throws ParseException {

		if (!timeSet.add(timeInfo))
			return false;

		Calendar calendar = Calendar.getInstance();
		// SimpleDateFormat sdf = new
		// SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		calendar.setTime(sdf.parse(timeInfo));
		System.out.println("parseTimeInfo: " + timeInfo);
		int year = calendar.get(Calendar.YEAR);
		int month = calendar.get(Calendar.MONTH);
		int day = calendar.get(Calendar.DAY_OF_MONTH);

		int hour = calendar.get(Calendar.HOUR);
		int minute = calendar.get(Calendar.MINUTE);
		int second = calendar.get(Calendar.SECOND);

		String date = year + "-" + month + "-" + day;
		rangePair.add(date);
		return true;
	}

	public static void main(String[] args) {
		// initialization
		pipeline = setupPipeline();
		timeSet = new HashSet<String>();
		rangePair = new ArrayList<String>();

		// read ant write file
		//String filename = "ViewItem.aspx";
		//String output = "./output/" + filename;
		try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(args[1], true)))) {
			//try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output, true)))) {
			String input = args[0];
			//String input = "./input/" + filename;
			System.out.println("--");
			System.out.println("Input File: " + input);
			System.out.println("--");
			BufferedReader inputStream = new BufferedReader(new FileReader(input));

			// System.out.println("\nContent: ");
			String line;
			int cnt = 0;
			while ((line = inputStream.readLine()) != null) {
				// System.out.println(line);
				annotateText(line, "");
			}
			String output = args[1];
			System.out.println("Output File: " + output);
			System.out.println("[" + rangePair.get(0) + " TO " + rangePair.get(1) + "]");
			out.println("[" + rangePair.get(0) + " TO " + rangePair.get(1) + "]");
		} catch (IOException e) {
			System.err.println("Caught IOException: " + e.getMessage());
		} finally {

		}
	}
}
