# Part 1: Question No 4

## Zero-order reseller(ques4.1)

A LEFT JOIN is used to find resellers who have never placed an order.

RS024 is the only reseller with no matching order.

## COUNT(*) vs COUNT(order_id)

For RS024, the LEFT JOIN keeps the reseller row even though there is no
matching order. The columns from the orders table are therefore NULL.

COUNT(*) counts the LEFT JOIN row, so:

COUNT(*) = 1

COUNT(order_id) only counts non-NULL order IDs, so:

COUNT(order_id) = 0

Therefore, COUNT(*) should not be used to identify zero matching orders.

The correct approach is:

WHERE o.order_id IS NULL