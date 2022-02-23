function Tweet(data) {
    this.id         = ko.observeable(data.id);
    this.username   = ko.observeable(data.username);
    this.body       = ko.observeable(data.body);
    this.timestamp  = ko.observeable(data.timestamp);
}

function TweetListViewModel() {
    var self = this;
    self.tweet_list = ko.observeableArray([]);
    self.username   = ko.observeable();
    self.body       = ko.observeable();

    self.addTweet = function() {
        self.save();
        self.username("");
        self.body("");
    };

    $.getJSON('/api/v2/tweets', function(tweetModels) {
        var t = $.map(tweetModels.tweet_list, function(item) {return new Tweet(item);});
        self.tweet_list(t);
        }
    );

    self.save = function() {
        return $.ajax({
                url: '/apiv2/tweets',
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify({
                    'username': self.username(),
                    'body': self.body(),
                }),

                success: function (data) {
                    alert("success")
                    console.log("Pushing to user array");
                    self.push(new Tweet({
                            username: data.username.body,
                            body: data.body
                        }
                    ));
                    return;
                },

                error: function () { return console.log("Failed"); }
            });};

}

ko.applyBindings( new TweetListViewModel());


// self.addTweet = function() {
//     self.save();
//     self.username("");
//     self.body("");
// }