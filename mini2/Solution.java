import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

class Solution {

    public static int minimizeCost(List<Integer> arr) {
        // Create a max-heap by negating values (because Java's PriorityQueue is a min-heap by default)
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);

        // Add all elements to the heap (negate the values)
        for (int num : arr) {
            maxHeap.add(-num); // Negate the values for max-heap behavior
        }

        int totalCost = 0; // Initialize the total cost

        // Continue until only one element remains in the heap
        while (maxHeap.size() > 1) {
            // Get the two largest elements (which are negated smallest elements)
            int first = -maxHeap.poll(); // Negate back to original value
            int second = -maxHeap.poll(); // Negate back to original value

            int cost = first + second; // Calculate the cost of this operation
            totalCost += cost; // Add the cost to the total cost

            // Push the combined value back into the heap (negate it)
            maxHeap.add(-cost); // Negate to maintain max-heap property
        }

        return totalCost; // Return the minimum total cost
    }

    public static void main(String[] args) {
        // Create a list of integers
        List<Integer> arr = new ArrayList<>();

        // Add elements to the list
        arr.add(30);
        arr.add(10);
        arr.add(20);

        // Call the minimizeCostBruteForce method
        int result = minimizeCost(arr);

        // Print the result
        System.out.println(result);
    }
}
