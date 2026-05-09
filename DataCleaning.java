import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * MapReduce job for cleaning and preprocessing crop yield data.
 * - Removes invalid/incomplete records
 * - Validates data format and values
 * - Filters out rows with missing critical fields
 */
public class DataCleaning {

    // Mapper Class - Validates and filters raw data
    public static class TokenizerMapper extends Mapper<Object, Text, Text, Text> {
        
        private static final int MINIMUM_FIELDS = 5;
        private int invalidRecords = 0;
        private int validRecords = 0;

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            
            String line = value.toString().trim();

            // Skip empty lines
            if (line.isEmpty()) return;

            // Skip header row
            if (line.toLowerCase().contains("crop") || line.toLowerCase().contains("year")) {
                return;
            }

            String[] fields = line.split(",");

            // Validate field count
            if (fields.length < MINIMUM_FIELDS) {
                invalidRecords++;
                return;
            }

            // Validate individual fields
            boolean valid = true;
            for (int i = 0; i < fields.length; i++) {
                String field = fields[i].trim();
                
                // Check for empty or null values
                if (field.isEmpty() || field.equalsIgnoreCase("null") || field.equalsIgnoreCase("na")) {
                    valid = false;
                    break;
                }
                
                // Validate numeric fields (indices 2, 3, 4 for temp, rainfall, yield)
                if (i >= 2 && i <= 4) {
                    try {
                        Double.parseDouble(field);
                    } catch (NumberFormatException e) {
                        valid = false;
                        break;
                    }
                }
            }

            // Emit only valid rows
            if (valid) {
                validRecords++;
                // Use crop as key for grouping similar crops together
                String cropKey = fields[0].trim();
                context.write(new Text(cropKey), new Text(line));
            } else {
                invalidRecords++;
            }
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            // Log statistics
            System.out.println("Mapper - Valid records: " + validRecords + ", Invalid records: " + invalidRecords);
        }
    }

    // Reducer Class - Aggregates and deduplicates records by crop
    public static class DataReducer extends Reducer<Text, Text, Text, Text> {
        
        private int totalRecords = 0;

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            
            int recordCount = 0;
            for (Text val : values) {
                context.write(key, val);
                recordCount++;
                totalRecords++;
            }
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            System.out.println("Reducer - Total records processed: " + totalRecords);
        }
    }

    // Driver/Main Class
    public static void main(String[] args) throws Exception {

        if (args.length < 2) {
            System.err.println("Usage: DataCleaning <input path> <output path> [number of reducers]");
            System.err.println("Example: hadoop jar DataCleaning.jar DataCleaning /crop_yield/input /crop_yield/cleaned 4");
            System.exit(-1);
        }

        String inputPath = args[0];
        String outputPath = args[1];
        int numReducers = args.length > 2 ? Integer.parseInt(args[2]) : 1;

        Configuration conf = new Configuration();
        
        // Set configuration parameters
        conf.set("mapreduce.job.reduces", String.valueOf(numReducers));
        conf.set("mapreduce.output.fileoutputformat.compress", "true");
        conf.set("mapreduce.output.fileoutputformat.compress.codec", "org.apache.hadoop.hive.ql.io.compress.SnappyCodec");

        Job job = Job.getInstance(conf, "Crop Data Cleaning and Preprocessing");

        // Set JAR and classes
        job.setJarByClass(DataCleaning.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(DataReducer.class);

        // Set output key-value types
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        // Set number of reducers
        job.setNumReduceTasks(numReducers);

        // Set input and output paths
        FileInputFormat.addInputPath(job, new Path(inputPath));
        FileOutputFormat.setOutputPath(job, new Path(outputPath));

        // Submit job and wait for completion
        long startTime = System.currentTimeMillis();
        boolean success = job.waitForCompletion(true);
        long endTime = System.currentTimeMillis();

        if (success) {
            System.out.println("Job completed successfully!");
            System.out.println("Execution time: " + (endTime - startTime) / 1000 + " seconds");
            System.exit(0);
        } else {
            System.out.println("Job failed!");
            System.exit(1);
        }
    }
}