#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <bits/stdc++.h> 
#include <chrono>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;
using namespace chrono;

unordered_map<string, pair<int, int>> TILE_LOCATIONS;
unordered_map<string, int> LINEAR_CONFLICTS;
string GOAL = "ABCDEFGHIJKLMNO.";
int SIZE = 4;
unordered_map<string, int> FOUR_LETTER_COMBOS;

class Triple
{
public:
    int data0;
    int data1;
    string data2;

    Triple(int a, int b, string c)
    {
        data0 = a;
        data1 = b;
        data2 = c;
    }
};

class myComparator
{
public:
    int operator() (const Triple& p1, const Triple& p2)
    {
        return p1.data0 > p2.data0;
    }
};

void initialize_maps()
{
    TILE_LOCATIONS["A"] = pair<int, int>(0, 0);
    TILE_LOCATIONS["B"] = pair<int, int>(0, 1);
    TILE_LOCATIONS["C"] = pair<int, int>(0, 2);
    TILE_LOCATIONS["D"] = pair<int, int>(0, 3);
    TILE_LOCATIONS["E"] = pair<int, int>(1, 0);
    TILE_LOCATIONS["F"] = pair<int, int>(1, 1);
    TILE_LOCATIONS["G"] = pair<int, int>(1, 2);
    TILE_LOCATIONS["H"] = pair<int, int>(1, 3);
    TILE_LOCATIONS["I"] = pair<int, int>(2, 0);
    TILE_LOCATIONS["J"] = pair<int, int>(2, 1);
    TILE_LOCATIONS["K"] = pair<int, int>(2, 2);
    TILE_LOCATIONS["L"] = pair<int, int>(2, 3);
    TILE_LOCATIONS["M"] = pair<int, int>(3, 0);
    TILE_LOCATIONS["N"] = pair<int, int>(3, 1);
    TILE_LOCATIONS["O"] = pair<int, int>(3, 2);

    LINEAR_CONFLICTS[""] = 0;
    LINEAR_CONFLICTS["<"] = 0;
    LINEAR_CONFLICTS[">"] = 1;
    LINEAR_CONFLICTS["<<<"] = 0;
    LINEAR_CONFLICTS["<<>"] = 1;
    LINEAR_CONFLICTS["><<"] = 1;
    LINEAR_CONFLICTS["<>>"] = 1;
    LINEAR_CONFLICTS[">><"] = 1;
    LINEAR_CONFLICTS[">>>"] = 2;
    LINEAR_CONFLICTS["<<<<<<"] = 0;
    LINEAR_CONFLICTS["<<<<<>"] = 1;
    LINEAR_CONFLICTS["<<<><<"] = 1;
    LINEAR_CONFLICTS["<<<<>>"] = 1;
    LINEAR_CONFLICTS["<<<>><"] = 1;
    LINEAR_CONFLICTS["<<<>>>"] = 2;
    LINEAR_CONFLICTS["><<<<<"] = 1;
    LINEAR_CONFLICTS["><<<<>"] = 2;
    LINEAR_CONFLICTS["<><><<"] = 1;
    LINEAR_CONFLICTS["<<><>>"] = 1;
    LINEAR_CONFLICTS["<><>><"] = 2;
    LINEAR_CONFLICTS["<<>>>>"] = 2;
    LINEAR_CONFLICTS[">><<<<"] = 1;
    LINEAR_CONFLICTS["><><<>"] = 2;
    LINEAR_CONFLICTS[">><><<"] = 2;
    LINEAR_CONFLICTS["><><>>"] = 2;
    LINEAR_CONFLICTS["<>>>><"] = 2;
    LINEAR_CONFLICTS["<>>>>>"] = 2;
    LINEAR_CONFLICTS[">>><<<"] = 1;
    LINEAR_CONFLICTS[">>><<>"] = 2;
    LINEAR_CONFLICTS[">>>><<"] = 2;
    LINEAR_CONFLICTS[">>><>>"] = 2;
    LINEAR_CONFLICTS[">>>>><"] = 2;
    LINEAR_CONFLICTS[">>>>>>"] = 3;
}

int conflict(string row)
{
    string code_string = "";
    if(row.length() == 0)
       return LINEAR_CONFLICTS[""];
    for(int i = 0; i < row.length() - 1; i++)
    {
        for(int j = i + 1; j < row.length(); j++)
        {
            if(row[i] > row[j])
                code_string += ">";
            else
                code_string += "<";
        }
    }
    return LINEAR_CONFLICTS[code_string];
}

string helper_row_2(int i, string row)
{
    string r = "";
    for(int col = 0; col < SIZE; col++)
    {   
        string letter = row.substr(col, 1);
        if(letter != ".")
        {
            int actual_row = TILE_LOCATIONS[letter].first;
            if(i == actual_row)
                r += letter;
        }
    }
    return r;
}

string helper_col_2(int i, string col)
{
    string c = "";
    for(int row = 0; row < SIZE; row++)
    {
        string letter = col.substr(row, 1);
        if(letter != ".")
        {
            int actual_col = TILE_LOCATIONS[letter].second;
            if(i == actual_col)
                c += letter;
        }
    }
    return c;
}

string helper_row(int i, string board)
{
    string r = "";
    for(int j = 0; j < SIZE; j++)
        r += board.substr(i * SIZE + j, 1);
    return r;
}

string helper_col(int i, string board)
{
    string c = "";
    for(int j = 0; j < SIZE; j++)
        c += board.substr(j * SIZE + i, 1);
    return c;
}

int conflict_heuristic(string board)
{
    int heuristic = 0;
    // do the rows first
    for(int row = 0; row < SIZE; row++)
    {
        string t = to_string(row) + " " + "r" + " " + helper_row(row, board);
        heuristic += FOUR_LETTER_COMBOS[t];
    }
    // columns next
    for(int col = 0; col < SIZE; col++)
    {
        string t = to_string(col) + " " + "c" + " " + helper_col(col, board);
        heuristic += FOUR_LETTER_COMBOS[t];
    }
    return heuristic;
}

vector<pair<string, int>> get_children(string board)
{
    vector<pair<string, int>> children;
    int ind = board.find(".");
    int a = ind / SIZE;
    int b = ind % SIZE;
    if(b > 0)
    {
        int net_change = 1;
        int ind2 = ind - 1;
        string tile = board.substr(ind2, 1);
        int row = TILE_LOCATIONS[tile].first;
        int col = TILE_LOCATIONS[tile].second;
        if(col > b - 1)
            net_change = -1;
        string child = board.substr(0, min(ind, ind2)) + board.substr(max(ind, ind2), 1) + board.substr(min(ind, ind2) + 1, max(ind, ind2) - min(ind, ind2) - 1) + board.substr(min(ind, ind2), 1) + board.substr(max(ind, ind2) + 1, board.length() - max(ind, ind2) - 1);
        if(col == b - 1 || col == b)
            net_change += FOUR_LETTER_COMBOS[to_string(col) + " " + "c" + " " + helper_col(col, child)] - FOUR_LETTER_COMBOS[to_string(col) + " " + "c" + " " + helper_col(col, board)];
        children.push_back(pair<string, int>(child, net_change));
    }
    
    if(b < SIZE - 1)
    {
        int net_change = 1;
        int ind2 = ind + 1;
        string tile = board.substr(ind2, 1);
        int row = TILE_LOCATIONS[tile].first;
        int col = TILE_LOCATIONS[tile].second;
        if(col < b + 1)
            net_change = -1;
        string child = board.substr(0, min(ind, ind2)) + board.substr(max(ind, ind2), 1) + board.substr(min(ind, ind2) + 1, max(ind, ind2) - min(ind, ind2) - 1) + board.substr(min(ind, ind2), 1) + board.substr(max(ind, ind2) + 1, board.length() - max(ind, ind2) - 1);
        if(col == b + 1 || col == b)
            net_change += FOUR_LETTER_COMBOS[to_string(col) + " " + "c" + " " + helper_col(col, child)] - FOUR_LETTER_COMBOS[to_string(col) + " " + "c" + " " + helper_col(col, board)];
        children.push_back(pair<string, int>(child, net_change));
    }

    if(a < SIZE - 1)
    {
        int net_change = 1;
        int ind2 = ind + SIZE;
        string tile = board.substr(ind2, 1);
        int row = TILE_LOCATIONS[tile].first;
        int col = TILE_LOCATIONS[tile].second;
        if(round_toward_neg_infinity < a + 1)
            net_change = -1;
        string child = board.substr(0, min(ind, ind2)) + board.substr(max(ind, ind2), 1) + board.substr(min(ind, ind2) + 1, max(ind, ind2) - min(ind, ind2) - 1) + board.substr(min(ind, ind2), 1) + board.substr(max(ind, ind2) + 1, board.length() - max(ind, ind2) - 1);
        if(row == a + 1 || row == a)
            net_change += FOUR_LETTER_COMBOS[to_string(row) + " " + "r" + " " + helper_row(row, child)] - FOUR_LETTER_COMBOS[to_string(row) + " " + "r" + " " + helper_row(row, board)];
        children.push_back(pair<string, int>(child, net_change));
    }

    if(a > 0)
    {
        int net_change = 1;
        int ind2 = ind - SIZE;
        string tile = board.substr(ind2, 1);
        int row = TILE_LOCATIONS[tile].first;
        int col = TILE_LOCATIONS[tile].second;
        if(row > a - 1)
            net_change = -1;
        string child = board.substr(0, min(ind, ind2)) + board.substr(max(ind, ind2), 1) + board.substr(min(ind, ind2) + 1, max(ind, ind2) - min(ind, ind2) - 1) + board.substr(min(ind, ind2), 1) + board.substr(max(ind, ind2) + 1, board.length() - max(ind, ind2) - 1);
        if(row == a - 1 || row == a)
            net_change += FOUR_LETTER_COMBOS[to_string(row) + " " + "r" + " " + helper_row(row, child)] - FOUR_LETTER_COMBOS[to_string(row) + " " + "r" + " " + helper_row(row, board)];
        children.push_back(pair<string, int>(child, net_change));
    }

    return children;
}

bool parity_check(string board)
{
    vector<string> arr;
    int index = -1;
    for(int i = 0; i < board.length(); i++)
    {
        if(board.substr(i, 1) != ".")
            arr.push_back(board.substr(i, 1));
        else
            index = i;
    }
    int count = 0;
    for(int i = 0; i < board.length() - 2; i++)
        for(int j = i + 1; j < board.length() - 1; j++)
            if(arr[i] > arr[j])
                count += 1;
    int row_num = index / SIZE;          
    if(SIZE % 2 == 0)
        return (count - row_num + 1) % 2 == 0;
    else
        return count % 2 == 0;
}

int taxicab(int size, string board)
{
    int s = 0;
    string goal = GOAL;
    for(int i = 0; i < board.length(); i++)
    {
        if(board.substr(i) != ".")
        {
            int num = goal.find(board.substr(i));
            int row1 = num / size;
            int col1 = num % size;
            int row2 = i / size;
            int col2 = i % size;
            s += abs(col1 - col2) + abs(row1 - row2);
        }
    }
    return s;
}

void generate_combos()
{
    vector<string> letters;
    for(int i = 0; i < GOAL.length(); i++)
        letters.push_back(GOAL.substr(i, 1));
    for(int i = 0; i < SIZE; i++)
    {
        for(string l1 : letters)
        {
            for(string l2 : letters)
            {
                if(l2 != l1)
                {
                    for(string l3 : letters)
                    {
                        if(l3 != l2 && l3 != l1)
                        {
                            for(string l4 : letters)
                            {
                                if(l4 != l3 && l4 != l2 && l4 != l1)
                                {
                                    string s = l1 + l2 + l3 + l4;
                                    FOUR_LETTER_COMBOS[to_string(i) + " " + "r" + " " + s] = 2 * conflict(helper_row_2(i, s));
                                    FOUR_LETTER_COMBOS[to_string(i) + " " + "c" + " " + s] = 2 * conflict(helper_col_2(i, s));
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

int a_star(string board)
{
    if(!parity_check(board))
        return -1;
    unordered_set<string> closed;
    priority_queue<Triple, vector<Triple>, myComparator> fringe;
    // store in form (heuristic, depth, board)
    fringe.push(Triple(taxicab(SIZE, board) + conflict_heuristic(board), 0, board));
    while(fringe.empty() == false)
    {
        Triple state = fringe.top();
        fringe.pop();
        if(state.data2 == GOAL)
            return state.data1; // returns number of moves taken
        if(closed.find(state.data2) == closed.end()) // if not in closed
        {
            closed.insert(state.data2);
            for(pair<string, int> p : get_children(state.data2))
            {
                if(closed.find(p.first) == closed.end())
                {
                    Triple t2(
                        state.data0 + 1 + p.second, // new heuristic
                        state.data1 + 1, // 1 extra move was taken
                        p.first
                    );
                    fringe.push(t2);
                }
            }
        }
    }
    return -1;
}

int main()
{
    initialize_maps();
    cout<<"Finished initializing maps"<<"\n";
    auto start = high_resolution_clock::now();
    generate_combos();
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout<<"Finished generating all possible combinations for rows and columns"<<"\n";
    // auto start2 = high_resolution_clock::now();
    // int moves = a_star(".JAFNHBIOMKGLDEC");
    // auto end2 = high_resolution_clock::now();
    // auto duration2 = duration_cast<milliseconds>(stop - start);
    // cout<<duration2.count()<<" milliseconds"<<"\n";
    ifstream infile("15_puzzles.txt");
    string line;
    vector<string> puzzles;
    int count = 0;
    int count2 = 0;
    while(count2 < 30 && getline(infile, line))
    {
        puzzles.push_back(line.substr(0, 16));
        count2++;
    }
    int total = 0;
    for(string puzzle : puzzles)
    {
        auto start = high_resolution_clock::now();
        int moves = a_star(puzzle);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(stop - start);
        cout<<"Line "<<count<<" has "<<moves << " moves and ran in "<<duration.count()<<" milliseconds.\n";
        total += duration.count();
        count++;
    }
    cout<<total<<"\n";

    return 0;
}