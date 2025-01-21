#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <algorithm>
#include <sys/stat.h>
#include <chrono>

using namespace std;

unordered_map<string, int> calculate_repeat_offenders(const string& file_name) {
    unordered_map<string, int> plate_violations;

    ifstream file(file_name);
    if (!file.is_open()) {
        cerr << "Error: Could not open file." << endl;
        return plate_violations;
    }

    string line;
    while (getline(file, line)) {
        line.erase(remove(line.begin(), line.end(), '"'), line.end());

        stringstream ss(line);
        vector<string> tokens;
        string token;

        while (getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        if (tokens.size() > 1 && tokens[1] != "BLANKPLATE") {
            plate_violations[tokens[1]]++;
        }
    }

    file.close();
    return plate_violations;
}

int main() {
    string filename = "../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv";

    auto start_time = chrono::high_resolution_clock::now();
    auto repeat_offenders = calculate_repeat_offenders(filename);

    vector<pair<string, int>> sorted_offenders(repeat_offenders.begin(), repeat_offenders.end());
    sort(sorted_offenders.begin(), sorted_offenders.end(),
         [](const auto& a, const auto& b) { return a.second > b.second; });

    cout << "Repeat Offenders (Plate ID: Number of Violations):" << endl;
    for (int i = 0; i < 20 && i < sorted_offenders.size(); ++i) {
        cout << sorted_offenders[i].first << ": " << sorted_offenders[i].second << endl;
    }

    long tot_count = 0;
    for (const auto& entry : repeat_offenders) {
        if (entry.second > 1) {
            tot_count += 1;
        }
    }

    cout << "\nTotal number of repeat offenders: " << tot_count << endl;

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    cout << "\nExecution time: " << execution_time.count() << " seconds" << endl;

    return 0;
}
