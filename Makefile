build-packager:
	docker build -t lambda-hugo-packager .

package:
	docker run --rm -it \
					-e PROFILE=default \
					-e BUILD=0.0.7 \
					-e HUGO_VERSION=0.25.1 \
					-v ~/.aws:/root/.aws:ro \
					-v `pwd`/code:/code \
					-v `pwd`/build:/build \
					--entrypoint "/build_entry.sh" \
					lambda-hugo-packager
