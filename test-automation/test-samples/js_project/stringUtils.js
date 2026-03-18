/**
 * String utilities module
 */

/**
 * Reverse a string
 * @param {string} str - Input string
 * @returns {string} Reversed string
 */
function reverseString(str) {
  return str.split('').reverse().join('');
}

/**
 * Check if a string is a palindrome
 * @param {string} str - Input string
 * @returns {boolean} True if palindrome
 */
function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  return cleaned === reverseString(cleaned);
}

/**
 * Count words in a string
 * @param {string} str - Input string
 * @returns {number} Word count
 */
function countWords(str) {
  if (!str.trim()) return 0;
  return str.trim().split(/\s+/).length;
}

/**
 * Capitalize first letter of each word
 * @param {string} str - Input string
 * @returns {string} Title case string
 */
function toTitleCase(str) {
  return str.replace(/\w\S*/g, (txt) =
> 
    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
}

/**
 * String manipulator class
 */
class StringManipulator {
  constructor() {
    this.operations = [];
  }

  /**
   * Truncate string to max length
   * @param {string} str - Input string
   * @param {number} maxLength - Maximum length
   * @returns {string} Truncated string
   */
  truncate(str, maxLength) {
    this.operations.push('truncate');
    if (str.length 
<;= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  }

  /**
   * Get operation history
   * @returns {string[]} Operation names
   */
  getHistory() {
    return this.operations;
  }
}

module.exports = {
  reverseString,
  isPalindrome,
  countWords,
  toTitleCase,
  StringManipulator
};
