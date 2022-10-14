# ros2_kart_racing_action

A Github Action that is supposed to be used with the [kart_navigation-template repository](https://github.com/gstavrinos/kart_navigation-template). It runs your ROS2 `kart_navigation` package in the simulated environment provided by the [ros2_kart_racing repository](https://github.com/gstavrinos/ros2_kart_racing), and creates PR on its `leaderboards` branch with your personal record for each race track.

# Inputs
* A [secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `PAT`. This should be a [personal access token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) that has permissions for `public repos` (or the whole `repo` category for private repositories that use the `kart_navigation`). This is required because the action creates a fork under your username.
* A `track` name your `kart_navigation` package will be tested on. This is 100% taken care of in the `kart_navigation` template repository and *SHOULD NOT* be handled manually.

# Expected results (+ how to pass all tests)
## Failed test
* Your kart times out after 30 minutes of simulation time or 60 minutes of system time. Make sure your code is not too slow. (`DNF` print on action logs)
* Your code did not achieve a new personal record. (`No personal record` print on action logs)
* There was an other error while building or running your code. Make sure that everything is working locally, and if it does, maybe you need to create an issue on the corresponding repository.
## Successful test
**ONLY** when you achieve a personal record on **ALL** race tracks.

Based on the above, not having successful tests does not necessarily mean that there is a problem with your code.
