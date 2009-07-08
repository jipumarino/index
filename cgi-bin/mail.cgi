#!/usr/local/bin/perl
##############################################################################
# Variable de ubiación de sendmail:											 #
$mailprog = '/usr/sbin/sendmail';
# Receptor:
$recipient = 'jipumari@puc.cl';
# Path de la página
$webpath = 'http://www2.ing.puc.cl/~jipumari/enviado.html';
# Asunto del mensaje
$subject = 'I N D E X';
##############################################################################

# Parse Form Contents
&parse_form;

# Return HTML Page or Redirect User
&return_html;

# Send E-Mail
&send_mail;

sub parse_form {

    # Define the configuration associative array.                            #
    %Config = ('email','',              'realname','',    			'body','',);

    # Determine the form's REQUEST_METHOD (GET or POST) and split the form   #
    # fields up into their name-value pairs.  If the REQUEST_METHOD was      #
    # not GET or POST, send an error.                                        #
    if ($ENV{'REQUEST_METHOD'} eq 'GET') {
        # Split the name-value pairs
        @pairs = split(/&/, $ENV{'QUERY_STRING'});
    }
    elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
        # Get the input
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
 
        # Split the name-value pairs
        @pairs = split(/&/, $buffer);
    }

    # For each name-value pair:                                              #
    foreach $pair (@pairs) {

        # Split the pair up into individual variables.                       #
        local($name, $value) = split(/=/, $pair);
 
        # Decode the form encoding on the name and value variables.          #
        $name =~ tr/+/ /;
        $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        # If they try to include server side includes, erase them, so they
        # aren't a security risk if the html gets returned.  Another 
        # security hole plugged up.
        $value =~ s/<!--(.|\n)*-->//g;

		$Config{$name} = $value;
    }
}


sub return_html {
      	print "Location: ",$webpath,"\n\n";
}

sub send_mail {
    
    open(MAIL,"|$mailprog -t");

    print MAIL "To: $recipient\n";
    print MAIL "From: $Config{'email'} ($Config{'realname'})\n";

    print MAIL "Subject: $subject\n\n";

    print MAIL $Config{'body'};
}

