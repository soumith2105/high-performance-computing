#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <dirent.h>
#include <algorithm>

using namespace std;

vector<string> get_file_names(const string& directory_path) {
    vector<string> csv_files;
    for (const auto& entry : filesystem::recursive_directory_iterator(directory_path)) {
        if (entry.is_regular_file() && entry.path().extension() == ".csv") {
            csv_files.push_back(entry.path().string());
        }
    }
    return csv_files;
}

void process_file(const string& file_name, unordered_map<string, unordered_map<string, double>>& data) {
    ifstream file(file_name);
    string line;

    while (getline(file, line)) {
        line.erase(remove(line.begin(), line.end(), '"'), line.end());

        stringstream ss(line);
        vector<string> tokens;
        string token;

        while (getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        if (tokens.size() > 9) {
            string key = tokens[9] + " " + tokens[0] + " " + tokens[1];
            double concentration = stod(tokens[7]);
            string parameter = tokens[3];
            data[key][parameter] += concentration;
        }
    }
    file.close();
}

void calculate_max(const unordered_map<string, unordered_map<string, double>>& data, unordered_map<string, string>& max_data, int& thread_count) {
    vector<string> keys;
    for (const auto& it : data) {
        keys.push_back(it.first);
    }

    for (size_t i = 0; i < keys.size(); ++i) {
        const auto& key = keys[i];
        const auto& inner_map = data.at(key);

        double max_value = -INFINITY;
        string max_param;

        for (const auto& param : inner_map) {
            if (param.second > max_value) {
                max_value = param.second;
                max_param = param.first;
            }
        }
        max_data[key] = max_param;
    }
}

int main() {
    string directory_path = "../data/AirNow Fires/data/";
    auto start_time = chrono::high_resolution_clock::now();

    vector<string> file_names = get_file_names(directory_path);

    unordered_map<string, unordered_map<string, double>> data;
    unordered_map<string, string> max_data;

    int thread_count = 1;

    for (int i = 0; i < file_names.size(); i++) {
        process_file(file_names[i], data);
    }
    calculate_max(data, max_data, thread_count);

    for (const auto& entry : max_data) {
        cout << entry.first << " -> " << entry.second << endl;
    }

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    cout << "\nExecution time: " << execution_time.count() << " seconds" << endl;

    return 0;
}
