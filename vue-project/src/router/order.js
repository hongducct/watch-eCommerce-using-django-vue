const order = {
    path: '/customer/order',
    redirect: '/customer/order/all',
    component: () => import('../layouts/order.vue'),
    children: [
        {
            path: 'all',
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
            name: 'customer-order',
            component: () => import('../views/customer/order/index.vue')
        },
        {
            path: 'test',
            name: 'customer-test',
            component: () => import('../views/customer/test/index.vue')
        }
    ]
}

export default order;