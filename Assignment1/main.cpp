// PROBLEM DEFINITION
// ------------------
// Reverse each word in the input string.
// The order of the words will be unchanged.
// A word is made up of letters and/or numbers.
// Other characters (spaces, punctuation) will not be reversed.
// NOTES
// ------
// Write production quality code
// We prefer clarity over performance (though if you can achieve both - great!)
// You can use the language that best highlights your programming ability
// the template below is in C++
// A working solution is preferred (assert in main() should succeed)
// Bonus points for good tests

#include <cctype>
#include <cstddef>
#include <string>
#include <cassert>

std::string reverse_words(const std::string &str)
{
    // A word is made up of letters and/or numbers.
    std::string result = str;
    size_t n = result.size();

    for(size_t i = 0; i<n;)
    {
        // if it is not part of a word, skip
        if(!std::isalpha(result[i]) && !std::isdigit(result[i]))
        {
            i++;
            continue;
        }

        // start of word
        size_t left = i;

        // until end of word
        while(i < n && (std::isalpha(result[i]) || std::isdigit(result[i])))
        {
            i++;
        }

        // end of word
        size_t right = i - 1;

        // reverse word
        while (left<right)
        {
            std::swap(result[left], result[right]);
            left++;
            right--;
        }
    }

    return result;
}

int main()
{
    std::string test_str = "String; 2be reversed...";
    assert(reverse_words(test_str) == "gnirtS; eb2 desrever...");
    return 0;
}