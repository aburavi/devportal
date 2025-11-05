import Layout from '@/components/Layout/Layout';
import ErrorPage from '@/pages/Error/Error';
import UnAuthorizePage from '@/pages/Error/Unauthorized';
import DeniedPage from '@/pages/Error/Denied';

// Faqs
import FaqsPage from '@/pages/Faqs/Faqs';

// Siggen
import SigGenPage from '@/pages/SigGen/SigGen';

// MySiggen
import MySigGenPage from '@/pages/SigGen/MySigGen';

// Home
import AnalyticsPage from '@/pages/Home/Home';

// Profile
import ProfilePage from '@/pages/Profile/Profile';

// Apps
import AppsPage from '@/pages/Apps/Apps';
import ApprovedPage from '@/pages/Apps/Approved';

// MyApps
import MyAppsPage from '@/pages/Apps/MyApps';

// Users
import TenantsPage from '@/pages/Tenants/Tenants';

// Logs
import LogsPage from '@/pages/Logs/Logs';

// MyLogs
import MyLogsPage from '@/pages/Logs/MyLogs';

// Productions
import ProductionsPage from '@/pages/Productions/Productions';

// MyProductions
import MyProductionsPage from '@/pages/Productions/MyProductions';

// Documentations
import DocumentationsPage from '@/pages/Documentations/Documentations';
import MyDocumentationsPage from '@/pages/Documentations/MyDocumentations';

// Login/Logout
import LoginPage from '@/pages/Login/Login';
import LogoutPage from '@/pages/Login/Logout';
import ChangePasswordPage from '@/pages/Login/Change_password';

export default [
    {
      path: '/error',
      name: 'Error',
      component: ErrorPage,
    },
    {
      path: '/unauthorized',
      name: 'Unauthorized',
      component: UnAuthorizePage,
    },
    {
      path: '/denied',
      name: 'Denied',
      component: DeniedPage,
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage,
    },
    {
      path: '/logout',
      name: 'Logout',
      component: LogoutPage,
    },
    {
      path: '/changepassword',
      name: 'ChangePassword',
      component: ChangePasswordPage,
    },
    {
      path: '/app',
      name: 'Layout',
      meta: {
        requiresAuth: true,
        permissions: ['admin']
      },
      component: Layout,
      children: [
        {
          path: 'home',
          name: 'AnalyticsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: AnalyticsPage,
        },
        {
          path: 'profile',
          name: 'profilePage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: ProfilePage,
        },
        {
          path: 'tenants',
          name: 'TenantsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: TenantsPage,
        },
        {
          path: 'apps',
          name: 'AppsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: AppsPage,
        },
        {
          path: 'approved',
          name: 'ApprovedPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: ApprovedPage,
        },
        {
          path: 'productions',
          name: 'ProductionsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: ProductionsPage,
        },
        {
          path: 'documentations',
          name: 'DocumentationsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: DocumentationsPage,
        },
        {
          path: 'siggen',
          name: 'SigGenPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: SigGenPage,
        },
        {
          path: 'faqs',
          name: 'FaqsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: FaqsPage,
        },
        {
          path: 'logs',
          name: 'LogsPage',
          meta: {
            requiresAuth: true,
            permissions: ['admin']
          },
          component: LogsPage,
        },
      ],
    },
    {
      path: '/tenant',
      name: 'Layout',
      meta: {
        requiresAuth: true,
        permissions: ['tenant']
      },
      component: Layout,
      children: [
        {
          path: 'home',
          name: 'AnalyticsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: AnalyticsPage,
        },
        {
          path: 'profile',
          name: 'profilePage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: ProfilePage,
        },
        {
          path: 'apps',
          name: 'AppsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: MyAppsPage,
        },
        {
          path: 'productions',
          name: 'ProductionsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: MyProductionsPage,
        },
        {
          path: 'documentations',
          name: 'DocumentationsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: MyDocumentationsPage,
        },
        {
          path: 'siggen',
          name: 'SigGenPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: MySigGenPage,
        },
        {
          path: 'faqs',
          name: 'FaqsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: FaqsPage,
        },
        {
          path: 'logs',
          name: 'LogsPage',
          meta: {
            requiresAuth: true,
            permissions: ['tenant']
          },
          component: MyLogsPage,
        },
      ],
    },
  ]
