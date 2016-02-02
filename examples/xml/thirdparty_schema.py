#!/usr/bin/env python

from __future__ import print_function

EXAMPLE_DOCUMENT = """
<wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soapenv:mustUnderstand="1">
    <wsu:Timestamp xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="Timestamp-15452452">
        <wsu:Created>2016-02-01T10:14:54.517Z</wsu:Created>
        <wsu:Expires>2016-02-01T10:19:54.517Z</wsu:Expires>
    </wsu:Timestamp>
    <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Id="Signature-2088192064">
        <ds:SignedInfo>
            <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
            <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" />
            <ds:Reference URI="#Id-1052429873">
                <ds:Transforms>
                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
                </ds:Transforms>
                <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" />
                <ds:DigestValue>...</ds:DigestValue>
            </ds:Reference>
            <ds:Reference URI="#Timestamp-15452452">
                <ds:Transforms>
                    <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" />
                </ds:Transforms>
                <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" />
                <ds:DigestValue>...</ds:DigestValue>
            </ds:Reference>
        </ds:SignedInfo>
        <ds:SignatureValue>
...
        </ds:SignatureValue>
        <ds:KeyInfo Id="KeyId-8475839474">
            <wsse:SecurityTokenReference xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="STRId-680050181">
                <wsse:KeyIdentifier EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509SubjectKeyIdentifier">...</wsse:KeyIdentifier>
            </wsse:SecurityTokenReference>
        </ds:KeyInfo>
    </ds:Signature>
</wsse:Security>
"""


from spyne.util.xml import parse_schema_file


class NS:
    WSSE = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
    WSU = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
    DS = "http://www.w3.org/2000/09/xmldsig#"
    XSD = "http://www.w3.org/2001/XMLSchema"

files = {
    NS.WSSE: "wsse.xsd",
    NS.WSU: "wsu.xsd",
    NS.DS: "ds.xsd",
    NS.XSD: "xsd.xsd",
}

import logging
logging.basicConfig(level=logging.DEBUG)

parse_schema_file(files[NS.WSSE], files=files)


class InteropServiceWithHeader(ServiceBase):
    __out_header__ = OutHeader

    @rpc(_returns=InHeader)
    def echo_in_header(ctx):
        return ctx.in_header

    @rpc(_returns=OutHeader)
    def send_out_header(ctx):
        ctx.out_header = OutHeader()
        ctx.out_header.dt = datetime(year=2000, month=1, day=1)
        ctx.out_header.f = 3.141592653

        return ctx.out_header
