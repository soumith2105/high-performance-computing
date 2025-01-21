#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <omp.h>
#include <regex>

using namespace std;


string format_number(long number) {
    stringstream ss;
    ss.imbue(locale(""));
    ss << fixed << number;
    return ss.str();
}

void process_population_chunk(const vector<string>& chunk, unordered_map<string, long>& local_data) {
    const string HEADERS[] = {
        "1960", "1961", "1962", "1963", "1964", "1965", "1966", "1967", "1968", "1969",
        "1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979",
        "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989",
        "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999",
        "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
        "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019",
        "2020", "2021", "2022", "2023"
    };

    for (const string& line : chunk) {
        // Use regex to split by ","
        regex re(R"(",")");
        sregex_token_iterator it(line.begin(), line.end(), re, -1);
        sregex_token_iterator end;

        vector<string> tokens(it, end);

        for (auto &token : tokens) {
            token.erase(remove(token.begin(), token.end(), '"'), token.end());
        }

        if (tokens[0] == "Not classified") {
            continue;
        }

        size_t i = 4;
        while (i < tokens.size()) {
            if (!tokens[i].empty()) {
                long population = stol(tokens[i]);
                local_data[HEADERS[i - 4]] += population;
            }
            ++i;
        }
    }
}

void read_population_data(const string& file_name, unordered_map<string, long>& data, int num_threads) {
    ifstream file(file_name);
    string line;

    for (int i = 0; i < 5 && getline(file, line); ++i);

    vector<string> all_lines;
    while (getline(file, line)) {
        all_lines.push_back(line);
    }

    size_t chunk_size = all_lines.size() / num_threads;
    vector<vector<string>> chunks;
    
    for (int i = 0; i < num_threads; ++i) {
        size_t start_idx = i * chunk_size;
        size_t end_idx = (i == num_threads - 1) ? all_lines.size() : (i + 1) * chunk_size;
        chunks.push_back(vector<string>(all_lines.begin() + start_idx, all_lines.begin() + end_idx));
    }

    file.close();

    #pragma omp parallel num_threads(num_threads)
    {
        unordered_map<string, long> local_data;
        int thread_id = omp_get_thread_num();
        process_population_chunk(chunks[thread_id], local_data);

        #pragma omp critical
        {
            for (const auto& [year, population] : local_data) {
                data[year] += population;
            }
        }
    }
}

// Main function
int main() {
    string filename = "../data/worldbank population/API_SP.POP.TOTL_DS2_en_csv_v2_3401680/API_SP.POP.TOTL_DS2_en_csv_v2_3401680.csv";
    int num_threads = 4;

    auto start_time = omp_get_wtime();

    unordered_map<string, long> data;
    read_population_data(filename, data, num_threads);

    vector<pair<string, long>> sorted_data(data.begin(), data.end());
    sort(sorted_data.begin(), sorted_data.end());

    cout << "Total population by year:" << endl;
    for (const auto &[year, population] : sorted_data) {
        cout << year << ": " << format_number(population) << endl;
    }

    auto end_time = omp_get_wtime();
    cout << "\nExecution time: " << (end_time - start_time) << " seconds" << endl;
    cout << "Number of threads used: " << num_threads << endl;

    return 0;
}
