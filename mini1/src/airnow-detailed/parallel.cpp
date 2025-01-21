#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <filesystem>
#include <omp.h>
#include <chrono>

using namespace std;

struct DataPoint {
    string key;
    string parameter;
    double concentration;

    DataPoint(const string& k, const string& p, double c)
        : key(k), parameter(p), concentration(c) {}
};

vector<string> get_file_names(const string& directory_path) {
    vector<string> csv_files;
    for (const auto& entry : filesystem::recursive_directory_iterator(directory_path)) {
        if (entry.is_regular_file() && entry.path().extension() == ".csv") {
            csv_files.push_back(entry.path().string());
        }
    }
    cout << "Total number of files: " << csv_files.size() << endl;
    return csv_files;
}

const int BUFFER_SIZE = 512 * 1024; // 512KB buffer

void process_buffer(char* buffer, size_t size, vector<DataPoint>& data_points) {
    string key, parameter;
    double concentration;
    string token;
    vector<string> tokens;
    bool insideQuotes = false;

    for (size_t i = 0; i < size; ++i) {
        char c = buffer[i];

        if (c == '"') {
            insideQuotes = !insideQuotes;
            if (!insideQuotes) {
                tokens.push_back(token);
                token.clear();
            }
            continue;
        }

        if (insideQuotes && c != ',') {
            token += c;
        }
        
        // Check for new line
        if (c == '\n') {
            // Ensure we have enough tokens to process
            if (tokens.size() > 9) {
                key = tokens[9] + " " + tokens[0] + " " + tokens[1];
                concentration = stod(tokens[7]);
                parameter = tokens[3];
                if (concentration > 0) {
                    #pragma omp critical
                    {
                        data_points.emplace_back(key, parameter, concentration);
                    }
                }
            }
            tokens.clear();
        }
    }
}

void process_file(const string& file_name, vector<DataPoint>& data_points) {
    ifstream file(file_name, ios::in | ios::binary);
    cout << "Processing file: " << file_name << endl;
    if (!file) {
        cerr << "Error opening file: " << file_name << endl;
        return;
    }

    char buffer[BUFFER_SIZE];

    while (file) {
        file.read(buffer, BUFFER_SIZE);
        streamsize count = file.gcount();

        if (count == 0) break;

        process_buffer(buffer, count, data_points);
    }

    file.close();
}

void calculate_max(const vector<DataPoint>& data_points, unordered_map<string, string>& max_data) {
    unordered_map<string, double> max_concentration;

    for (const auto& data_point : data_points) {
        const auto& key = data_point.key;
        if (data_point.concentration > max_concentration[key]) {
            max_concentration[key] = data_point.concentration;
            max_data[key] = data_point.parameter; // Store the corresponding parameter
        }
    }
}

int main() {
    ios::sync_with_stdio(false);

    string directory_path = "../data/AirNow Fires/data/";
    double start_time = omp_get_wtime();

    vector<string> file_names = get_file_names(directory_path);

    vector<DataPoint> data_points; // Store DataPoint objects
    unordered_map<string, string> max_data;

    int thread_count = 4;

    // Process files in parallel
    #pragma omp parallel for num_threads(thread_count)
    for (int i = 0; i < file_names.size(); i++) {
        vector<DataPoint> local_data_points; // Local storage for each thread
        process_file(file_names[i], local_data_points);

        // Merge results into the shared data_points vector
        #pragma omp critical
        {
            data_points.insert(data_points.end(), local_data_points.begin(), local_data_points.end());
        }
    }

    // Calculate maximums
    calculate_max(data_points, max_data);

    for (const auto& entry : max_data) {
        cout << entry.first << " -> " << entry.second << endl;
    }

    cout << "Total number of unique keys processed: " << max_data.size() << endl;

    double end_time = omp_get_wtime();
    cout << "Time taken: " << (end_time - start_time) << " seconds" << endl;

    return 0;
}
