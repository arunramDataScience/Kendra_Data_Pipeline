from aws_cdk import (
    Stack,
    aws_kendra as kendra,
    aws_iam as iam,
)
from constructs import Construct


class KendraCrawlerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 👇 IAM Role for Kendra
        kendra_role = iam.Role(
            self, "KendraCrawlerRole",
            assumed_by=iam.ServicePrincipal("kendra.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKendraFullAccess")
            ]
        )

        # 👇 Kendra Index
        kendra_index = kendra.CfnIndex(
            self, "KendraIndex",
            edition="DEVELOPER_EDITION",
            name="Kendra-Combined-Index",
            role_arn=kendra_role.role_arn
        )

        # 👇 Web Crawler for HSSUS
        hssus_web_crawler = kendra.CfnDataSource(
            self, "HSSUSWebCrawler",
            index_id=kendra_index.attr_id,
            name="HSSUS-Web-Crawler",
            type="WEBCRAWLER",
            role_arn=kendra_role.role_arn,
            data_source_configuration=kendra.CfnDataSource.DataSourceConfigurationProperty(
                web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                    urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["https://www.hssus.org/"]
                        )
                    ),
                    crawl_depth=2,
                    max_links_per_page=50,
                    max_content_size_per_page_in_mega_bytes=5.0,
                    url_exclusion_patterns=[".*(/calendar|/login).*"]
                )
            )
        )

        hssus_web_crawler.add_dependency(kendra_index)

        # 👇 Web Crawler for SewaUSA
        sewa_web_crawler = kendra.CfnDataSource(
            self, "SewaUSAWebCrawler",
            index_id=kendra_index.attr_id,
            name="SewaUSA-Web-Crawler",
            type="WEBCRAWLER",
            role_arn=kendra_role.role_arn,
            data_source_configuration=kendra.CfnDataSource.DataSourceConfigurationProperty(
                web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                    urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["https://www.sewausa.org/"]
                        )
                    ),
                    crawl_depth=2,
                    max_links_per_page=50,
                    max_content_size_per_page_in_mega_bytes=5.0,
                    url_exclusion_patterns=[".*(/calendar|/login).*"]
                )
            )
        )

        sewa_web_crawler.add_dependency(kendra_index)

        print("✅ AWS Kendra Crawlers (HSSUS & SewaUSA) defined successfully!")
