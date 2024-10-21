const customer = {
    path: '/customer',
    redirect: '/customer/account',
    component: () => import('../layouts/customer.vue'),
    children: [
        {
            path: 'account',
            name: 'customer-account',
            component: () => import('../views/customer/account/index.vue')
        },
        {
            path: 'notification',
            name: 'customer-notification',
            component: () => import('../views/customer/notification/index.vue')
        },
        {
            path: 'address',
            name: 'customer-address',
            component: () => import('../views/customer/address/index.vue')
        },
        {
            path: 'order',
            // path: '/orders/:status?', // Optional status parameter
            name: 'customer-order',
            component: () => import('../views/customer/order/index.vue')
        },
        {
            path: '/orders/:id/', // Dynamic route for order details
            name: 'order-detail',
            // component: OrderDetail // Your component to display order details
            component: () => import('../views/customer/order/OrderDetail.vue')
        },
        {
            path: 'test',
            name: 'customer-test',
            component: () => import('../views/customer/test/index.vue')
        }
    ]
}

export default customer;