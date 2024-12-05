/*
Implement Hash table.
Pick 20 random words.  Each word must be of different lengths, maximum length 8 characters  and minimum length 3 characters. 
By random I do not mean some random program, I mean just pick some workds of various lengths as mentioned.
The words will be of letters a-zA-Z and [the space character]?.

Insert them into a hash table. 
You can use a library for only the hash function.
The collision resolution scheme should be [open addressing - quadratic].

Initially the table size is 31.  The program should increase the table size and rehash at load factor of .5
So after you inserted about 15 or 16 words, 
your program automatically doubles the table size and re-inserts (automatically) 
the old words and then continue the insert of additional words.

You do not have to insert the words manually (one by one) but you can add the 
words in a file and let your program read from the file

At the end print the total number of collisions you get.
Submit your code and print screen of your execution
*/

#include <stdio.h>
#include <iostream>
#include <string>

using namespace std;

const string NULL_ITEM = "";

class HashTable {
private:
    int size;
    int count; // number of elements in the table
    int collisions;
    string* table;
    int hash(string key);
    void rehash();
    int nextPrime(int n);
public:
    HashTable(int _size);
    ~HashTable(); // destructor used when rehashing
    void insert(string key);
    void print();
};

HashTable::HashTable(int _size) {
    size = _size;
    count = 0;
    collisions = 0;
    table = new string[size]; // allocate memory for the table
    for (int i = 0; i < size; i++) {
        table[i] = NULL_ITEM;
    }
}

HashTable::~HashTable() {
    delete[] table;
}

void HashTable::insert(string key) {
    int index = hash(key);
    if (table[index] == NULL_ITEM) {
        table[index] = key;
    } else {
        collisions++;
        // quadratic probing
        int i = 1;
        while (table[index] != NULL_ITEM) {
            index = (index + i*i) % size; // CHECK THIS
            i++;
        }
        table[index] = key;
    }
    count++;
    if (count > size/2) {
        rehash();
    }
}

void HashTable::rehash() {
    int oldSize = size;
    size = nextPrime(size*2);
    count = 0;
    string* oldTable = table;
    table = new string[size];
    for (int i = 0; i < size; i++) {
        table[i] = NULL_ITEM;
    }
    for (int i = 0; i < oldSize; i++) {
        if (oldTable[i] != NULL_ITEM) {
            insert(oldTable[i]);
        }
    }
    delete[] oldTable;
}

int HashTable::hash(string key) {
    int hashVal = 0;
    for (int i = 0; i < key.length(); i++) {
        hashVal = (hashVal * 256 + key[i]) % size;
    }
    return hashVal;
}

int HashTable::nextPrime(int n) {
    int i = n + 1;
    while (true) {
        bool isPrime = true;
        for (int j = 2; j < i; j++) {
            if (i % j == 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) {
            return i;
        }
        i++;
    }
}

void HashTable::print() {
    cout << "Table:" << endl;
    for (int i = 0; i < size; i++) {
        cout << i << ": " << table[i] << endl;
    }
    cout << "Number of collisions: " << collisions << endl;
}

int main() {
    HashTable table(31);

    freopen("words.txt", "r", stdin);
    
    string line;
    while (getline(cin, line)) {
        table.insert(line);
    }

    table.print();
}