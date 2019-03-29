# Proxy Endpoint Example

## Who is this for?:

> This is for applications that need to process data via third party APIs. There is the option
> of manipulating data flowing to and from the third party API endpoints within our endpoint.
>
> For example, the Goose project has an endpoint that accepts requests for insurance policy
> creation. The logic in the endpoint validates the data in the request, creates an internal record
> in the data base for the policy, then forwards the data to a TuGo endpoint that creates the actual
> policy within the TuGo system. The TuGo endpoint then returns information such as the newly
> generated policy and pricing. The Goose endpoint logic updates the internal policy with the
> data returned by TuGo, and then responds with a success or error message.
>
> The proxyexample implementation is kept simple. There is no manipulation of the data during the
> processing. This example does a straight pass thru of a request to a third party endpoint, and
> returns the data as is. It is merely a starting point for handling proxy API calls.
