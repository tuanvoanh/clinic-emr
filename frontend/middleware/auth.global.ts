export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth();

  // If user is not authenticated and trying to access a protected page
  if (!isAuthenticated.value && to.path !== '/login') {
    return navigateTo('/login');
  }

  // If user is already authenticated and visits login page, redirect to home
  if (isAuthenticated.value && to.path === '/login') {
    return navigateTo('/');
  }
});
