# Contribution getting started

Contributions are highly welcomed and appreciated.  Every little bit of help counts,
so do not hesitate!

## Feature requests and feedback

Do you like pytest_otel?  Share some love on Twitter or in your blog posts!

We'd also like to hear about your propositions and suggestions.  Feel free to
[submit them as issues](https://github.com/kuisathaverat/pytest_otel/issues) and:

* Explain in detail how they should work.
* Keep the scope as narrow as possible.  This will make it easier to implement.

## Report bugs

Report bugs for pytest_otel in the [issue tracker](https://github.com/kuisathaverat/pytest_otel/issues)_.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting,
  specifically the Python interpreter version, installed libraries, pytest, and pytest_otel
  version.
* Detailed steps to reproduce the bug.

If you can write a demonstration test that currently fails but should pass
(xfail), that is a very useful commit to make as well, even if you cannot
fix the bug itself.

## Fix bugs

Look through the [GitHub issues for bugs](https://github.com/kuisathaverat/pytest_otel/issues?q=is%3Aopen+is%3Aissue+label%3Abug)
See also the ["good first issue" issues](hhttps://github.com/kuisathaverat/pytest_otel/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
that are friendly to new contributors.

> [!NOTE]
>`Talk <contact>` to developers to find out how you can fix specific bugs. To indicate that you are going
>to work on a particular issue, add a comment to that effect on the specific issue.

## Implement features

Look through the [GitHub issues for enhancements](https://github.com/kuisathaverat/pytest_otel/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)

> [!NOTE]
>`Talk <contact>` to developers to find out how you can implement specific features.

## Write documentation

Pytest Opentelemetry plugin could always use more documentation.  What exactly is needed?

* More complementary documentation.  Have you perhaps found something unclear?
* Documentation translations.  We currently have only English.
* Docstrings.  There can never be too many of them.
* Blog posts, articles and such -- they're all very appreciated.

## Preparing Pull Requests

* Fork the repository and create a new branch.
* Make sure your code is well tested.
* Ensure your code follows the Python style guide.
  * Run `make lint` to check your code.
  * Run `make format` to format your code.
* Ensure your code is well documented.
* Ensure the test suite passes.
  * Run `make test` to run the test suite.
  * Run `make it-test` to run the integration test suite.
* Use pre-commit hooks to ensure your code is well formatted and linted.
  * Run `pre-commit install` to install the pre-commit hooks.
  * Run `pre-commit run --all-files` to run the pre-commit hooks.
* Make sure your commits are well documented.
* Submit a pull request.

## Handling stale issues/PRs

Stale issues/PRs are those where contributors have asked for questions/changes
and the authors didn't get around to answer/implement them yet after a somewhat long time, or
the discussion simply died because people seemed to lose interest.

There are many reasons why people don't answer questions or implement requested changes:
they might get busy, lose interest, or just forget about it,
but the fact is that this is very common in open source software.

We really appreciates every issue and pull request, but being a high-volume project
with many issues and pull requests being submitted daily, we try to reduce the number of stale
issues and PRs by regularly closing them. When an issue/pull request is closed in this manner,
it is by no means a dismissal of the topic being tackled by the issue/pull request, but it
is just a way for us to clear up the queue and make the maintainers' work more manageable. Submitters
can always reopen the issue/pull request in their own time later if it makes sense.

### When to close

Here are a few general rules the maintainers use deciding when to close issues/PRs because
of lack of inactivity:

* Issues labeled ``question`` or ``needs information``: closed after 14 days inactive.
* Issues labeled ``proposal``: closed after six months inactive.
* Pull requests: after one month, consider pinging the author, update linked issue, or consider closing. For pull requests which are nearly finished, the team should consider finishing it up and merging it.

The above are **not hard rules**, but merely **guidelines**, and can be (and often are!) reviewed on a case-by-case basis.

### Closing pull requests

When closing a Pull Request, it needs to be acknowledging the time, effort, and interest demonstrated by the person which submitted it. As mentioned previously, it is not the intent of the team to dismiss a stalled pull request entirely but to merely to clear up our queue, so a message like the one below is warranted when closing a pull request that went stale:

    Hi <contributor>,

    First of all, we would like to thank you for your time and effort on working on this, we deeply appreciates it.

    We noticed it has been awhile since you have updated this PR, however. It is hard for us maintainers to track which PRs are ready for merging, for review, or need more attention.

    So for those reasons we, think it is best to close the PR for now, but with the only intention to clean up our queue, it is by no means a rejection of your changes. We still encourage you to re-open this PR (it is just a click of a button away) when you are ready to get back to it.

    Again we appreciate your time for working on this, and hope you might get back to this at a later time!

    <bye>

### Closing Issues

When a pull request is submitted to fix an issue, add text like ``closes #XYZW`` to the PR description and/or commits (where ``XYZW`` is the issue number). See the [GitHub docs](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) for more information.

When an issue is due to user error (e.g. misunderstanding of a functionality), please politely explain to the user why the issue raised is really a non-issue and ask them to close the issue if they have no further questions. If the original requestor is unresponsive, the issue will be handled as described in the section [Handling stale issues/PRs](#handling-stale-issuesprs) above.
