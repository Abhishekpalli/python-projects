import java.util.*;

public class demo {
    public static void main(String[] args){
        int[] arr = new int[4];
        int[] arr2 = {1,2,99,3,4,10,5,9};
        // int maxNum = maxArray(arr2);
        // System.out.println(maxNum);
        reverseArray(arr2);
        System.out.println(Arrays.toString(arr2));

    }
    public static void reverseArray(int[] arr){
        int l = 0;
        int r = arr.length - 1;
        while (l<r) {
            int temp = arr[l];
            arr[l] = arr[r];
            arr[r] = temp;
            l++;
            r--;
        }
        
    }
    public static int maxArray(int[] arr){
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }
}