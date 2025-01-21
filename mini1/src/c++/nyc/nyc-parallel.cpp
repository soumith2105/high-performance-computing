#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <omp.h>
#include <algorithm>
#include <sys/stat.h>
#include <chrono>

using namespace std;

unordered_map<string, int> calculate_repeat_offenders(const string& file_name, int num_threads) {
    unordered_map<string, int> plate_violations;
    omp_lock_t writelock;
    omp_init_lock(&writelock);

    struct stat file_stat;
    stat(file_name.c_str(), &file_stat);
    size_t file_size = file_stat.st_size;

    size_t chunk_size = file_size / num_threads;

    #pragma omp parallel num_threads(num_threads)
    {
        ifstream file(file_name);
        file.seekg(omp_get_thread_num() * chunk_size);

        string line;
        bool first_line = true;

        unordered_map<string, int> local_plate_violations;

        while (getline(file, line)) {
            if (first_line && omp_get_thread_num() != 0) {
                first_line = false;
                continue;
            }

            line.erase(remove(line.begin(), line.end(), '"'), line.end());

            stringstream ss(line);
            vector<string> tokens;
            string token;

            while (getline(ss, token, ',')) {
                tokens.push_back(token);
            }

            if (tokens.size() > 1 && tokens[1] != "BLANKPLATE") {
                local_plate_violations[tokens[1]]++;
            }

            if (file.tellg() >= (omp_get_thread_num() + 1) * chunk_size) {
                break;
            }
        }

        file.close();
        omp_set_lock(&writelock);
        for (const auto& entry : local_plate_violations) {
            plate_violations[entry.first] += entry.second;
        }
        omp_unset_lock(&writelock);
    }

    omp_destroy_lock(&writelock);
    return plate_violations;
}

int main() {
    string filename = "../data/nyc/parkingviolations/Parking_Violations_Issued_-_Fiscal_Year_2022.csv";
    int num_threads = 10;

    auto start_time = chrono::high_resolution_clock::now();
    auto repeat_offenders = calculate_repeat_offenders(filename, num_threads);

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
            tot_count+=1;
        }
    }

    cout << "\nTotal number of repeat offenders: " << tot_count << endl;

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    cout << "\nExecution time: " << execution_time.count() << " seconds" << endl;

    return 0;
}
